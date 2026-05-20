from abstracts.repository import BaseRepository
import re


_IDENT_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
_FIELD_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)?$")
_OPERATORS = {"=", "<>", "!=", ">", "<", ">=", "<="}
_JOIN_TYPES = {
    "join": "JOIN",
    "inner": "INNER JOIN",
    "inner join": "INNER JOIN",
    "left": "LEFT JOIN",
    "left join": "LEFT JOIN",
    "right": "RIGHT JOIN",
    "right join": "RIGHT JOIN",
}


class ResolverDynamicSqlRepository(BaseRepository):

    @staticmethod
    def _read(source, key: str, default=None):
        if isinstance(source, dict):
            return source.get(key, default)
        return getattr(source, key, default)

    @classmethod
    def _read_any(cls, source, keys: tuple[str, ...], default=None):
        for key in keys:
            value = cls._read(source, key, None)
            if value is not None and value != "":
                return value
        return default

    @staticmethod
    def _safe_ident(value: str, label: str) -> str:
        if not isinstance(value, str) or not _IDENT_RE.fullmatch(value):
            raise ValueError(f"{label} invalido: {value}")
        return value

    @staticmethod
    def _safe_field(value: str, label: str) -> str:
        if not isinstance(value, str) or not _FIELD_RE.fullmatch(value):
            raise ValueError(f"{label} invalido: {value}")
        return value

    def _build_from(self, data) -> str:
        tabela = self._safe_ident(self._read(data, "tabela", ""), "tabela")
        alias = self._read(data, "alias", None)
        if alias is None or alias == "":
            return tabela
        alias = self._safe_ident(alias, "alias")
        return f"{tabela} {alias}"

    def _build_join_on(self, on_list, param_counter) -> tuple[str, dict]:
        if not isinstance(on_list, list) or len(on_list) == 0:
            raise ValueError("join.on deve ser uma lista com ao menos uma condicao")

        clauses = []
        params = {}
        for item in on_list:
            esquerda_raw = self._read_any(
                item, ("esquerda", "left", "campo_esquerda"), None
            )
            if esquerda_raw is None:
                raise ValueError("join.on exige esquerda")

            esquerda = self._safe_field(esquerda_raw, "join.esquerda")
            operador = self._read_any(item, ("operador", "operator", "op"), "=")
            if operador not in _OPERATORS:
                raise ValueError(f"operador de join invalido: {operador}")

            direita_raw = self._read_any(
                item, ("direita", "right", "campo_direita"), None
            )
            if direita_raw is not None:
                direita = self._safe_field(direita_raw, "join.direita")
                clauses.append(f"{esquerda} {operador} {direita}")
                continue

            valor_raw = self._read_any(
                item, ("valor", "value", "direita_valor", "right_value"), None
            )
            if valor_raw is None:
                raise ValueError("join.on exige direita ou valor")

            param_name = f"join_valor_{param_counter['i']}"
            param_counter["i"] += 1
            params[param_name] = valor_raw
            clauses.append(f"{esquerda} {operador} :{param_name}")

        return " AND ".join(clauses), params

    def _build_joins(self, data, param_counter) -> tuple[str, dict]:
        joins = self._read(data, "joins", None)
        if not joins:
            return "", {}
        if not isinstance(joins, (list, tuple)):
            raise ValueError("joins deve ser uma lista")

        parts = []
        params = {}
        for join in joins:
            tipo = str(self._read(join, "tipo", "left")).strip().lower()
            join_sql = _JOIN_TYPES.get(tipo)
            if not join_sql:
                raise ValueError(f"tipo de join invalido: {tipo}")

            tabela = self._safe_ident(
                self._read_any(join, ("tabela", "table", "from"), ""), "join.tabela"
            )
            alias = self._read(join, "alias", None)
            if alias is None or alias == "":
                target = tabela
            else:
                target = f"{tabela} {self._safe_ident(alias, 'join.alias')}"

            on_sql, on_params = self._build_join_on(
                self._read(join, "on", None), param_counter
            )
            params.update(on_params)
            parts.append(f"{join_sql} {target} ON {on_sql}")

        return "\n".join(parts), params

    def execute(self, data):

        # ===============================
        # Monta o sql de acordo com os dados informados
        # ===============================
        campo = self._safe_field(self._read(data, "campo", ""), "campo")
        campo_id_raw = self._read(data, "campo_id", None)
        campo_id_valor = self._read(data, "campo_id_valor", None)
        from_sql = self._build_from(data)
        param_counter = {"i": 1}
        joins_sql, joins_params = self._build_joins(data, param_counter)

        where_sql = ""
        order_sql = ""
        params = {}
        if campo_id_raw not in (None, "") and campo_id_valor is not None:
            campo_id = self._safe_field(campo_id_raw, "campo_id")
            where_sql = f"WHERE {campo_id} = :campo_id_valor"
            params["campo_id_valor"] = campo_id_valor
            order_sql = f"ORDER BY {campo_id} DESC"

        sql = f"""
                        SELECT
                            {campo} as valor
                        FROM {from_sql}
                        {joins_sql}
                        {where_sql}
                        {order_sql}
                    """
        params.update(joins_params)

        # ===============================
        # 1) Executa a query
        # ===============================
        response = self.fetch_one(sql, params)

        # ===============================
        # 3) Retorno seguro
        # ===============================
        return response
