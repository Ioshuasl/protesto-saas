from __future__ import annotations

from typing import Any

from abstracts.repository import BaseRepository
from actions.data.query_params_parser import QueryParams, QueryParamsParser
from database.orm_firebird import normalize_row_keys
from packages.v1.administrativo.repositories.p_pessoa.p_pessoa_count_titulos_by_pessoa_ids_repository import (
    CountTitulosByPessoaIdsRepository,
)
from packages.v1.administrativo.schemas.p_pessoa_schema import (
    CNPJ_DIGITOS,
    CPF_DIGITOS,
    PPessoaIndexSchema,
    TIPO_PESSOA_FISICA,
    TIPO_PESSOA_JURIDICA,
    infer_tipo_pessoa_from_cpfcnpj,
    map_pessoa_row,
)

_PPESSOA_SORT_FIELD_MAP = {
    "pessoa_id": "PESSOA_ID",
    "nome": "NOME",
    "cpfcnpj": "CPFCNPJ",
    "cidade": "CIDADE",
    "uf": "UF",
    "telefone": "TELEFONE",
}

# CPFCNPJ e TELEFONE são VARCHAR(15) — LIKE com % nos dois lados estoura o bind.
_VARCHAR_15_LIKE_PREFIX_MAX = 14

# Limite por ramo da busca unificada (nome → cpfcnpj → telefone).
_BUSCA_BRANCH_LIMIT = 1000

_SELECT_COLUMNS = """
    PESSOA_ID,
    NOME,
    CPFCNPJ,
    ENDERECO,
    BAIRRO,
    CIDADE,
    UF,
    CEP,
    TELEFONE,
    RG,
    OBSERVACOES,
    BANCO,
    AGENCIA,
    CONTA,
    NOME_BANCO,
    NACIONALIDADE,
    ESTADO_CIVIL_ID,
    PROFISSAO_ID,
    CIDADE_AGENCIA,
    DATA_NASCIMENTO,
    EMAIL,
    CIDADE_ID,
    DATA_VALIDADE,
    MICRO_EMPRESA,
    CHAVE_PESSOA_IMP,
    COD_CRA,
    NOME_FANTASIA
"""


def _digits_only(value: str) -> str:
    return "".join(ch for ch in value if ch.isdigit())


def _varchar15_like_prefix(value: str) -> str:
    compact = _digits_only(value) or value.strip()
    return f"{compact[:_VARCHAR_15_LIKE_PREFIX_MAX]}%"


_CPFCNPJ_STRIP_CHARS = ".-/ \\(),"


def _select_columns_sql(alias: str | None = None) -> str:
    columns = [line.strip().rstrip(",") for line in _SELECT_COLUMNS.strip().splitlines()]
    if alias is None:
        return _SELECT_COLUMNS.strip()
    return ",\n            ".join(f"{alias}.{column} AS {column}" for column in columns)


def _normalized_cpfcnpj_sql(alias: str | None = None) -> str:
    prefix = f"{alias}." if alias else ""
    expr = f"TRIM(COALESCE({prefix}CPFCNPJ, ''))"
    for char in _CPFCNPJ_STRIP_CHARS:
        expr = f"REPLACE({expr}, '{char}', '')"
    return expr


def _cpfcnpj_digits_length_sql(alias: str | None = None) -> str:
    return f"CHAR_LENGTH({_normalized_cpfcnpj_sql(alias)})"


def _tipo_pessoa_digit_length(tipo_pessoa: str) -> int:
    if tipo_pessoa == TIPO_PESSOA_FISICA:
        return CPF_DIGITOS
    if tipo_pessoa == TIPO_PESSOA_JURIDICA:
        return CNPJ_DIGITOS
    raise ValueError(f"Tipo de pessoa inválido: {tipo_pessoa}")


class IndexRepository(BaseRepository):
    def execute(
        self,
        pessoa_index_schema: PPessoaIndexSchema,
        query_params: QueryParams,
    ) -> dict[str, Any]:
        page = query_params.page
        per_page = query_params.per_page
        sort_field, sort_direction = QueryParamsParser.resolve_sort(
            query_params,
            primary_key="pessoa_id",
            field_map=_PPESSOA_SORT_FIELD_MAP,
        )

        if pessoa_index_schema.busca:
            return self._execute_busca_unificada(
                pessoa_index_schema,
                page,
                per_page,
                sort_field,
                sort_direction,
            )

        return self._execute_sql(
            pessoa_index_schema, page, per_page, sort_field, sort_direction
        )

    def _execute_busca_unificada(
        self,
        pessoa_index_schema: PPessoaIndexSchema,
        page: int,
        per_page: int,
        sort_field: str,
        sort_direction: str,
    ) -> dict[str, Any]:
        busca = pessoa_index_schema.busca or ""
        seen_ids: set[int] = set()
        merged: list[dict[str, Any]] = []

        for fetch_fn in (
            self._fetch_rows_by_nome,
            self._fetch_rows_by_cpfcnpj,
            self._fetch_rows_by_telefone,
        ):
            rows = fetch_fn(pessoa_index_schema, busca, seen_ids)
            for row in rows:
                pessoa_id = row.get("pessoa_id")
                if pessoa_id is None or pessoa_id in seen_ids:
                    continue
                seen_ids.add(int(pessoa_id))
                merged.append(row)

        merged = self._filter_rows_by_tipo_pessoa(merged, pessoa_index_schema)
        merged = self._group_rows_by_cpfcnpj(merged)
        merged = self._sort_rows(merged, sort_field, sort_direction)
        total = len(merged)
        offset = (page - 1) * per_page
        page_rows = merged[offset : offset + per_page]

        return {
            "rows": self._enrich_rows_with_total_titulos(page_rows),
            "pagination": self._build_pagination_meta(page, per_page, total),
        }

    def _fetch_rows_by_nome(
        self,
        schema: PPessoaIndexSchema,
        busca: str,
        exclude_ids: set[int],
    ) -> list[dict[str, Any]]:
        where, params = self._build_location_sql_filters(schema)
        where.append("UPPER(NOME) LIKE UPPER(:busca_nome)")
        params["busca_nome"] = f"%{busca}%"
        self._append_exclude_ids(where, exclude_ids, params, "nome")
        return self._fetch_rows_limited(where, params)

    def _fetch_rows_by_cpfcnpj(
        self,
        schema: PPessoaIndexSchema,
        busca: str,
        exclude_ids: set[int],
    ) -> list[dict[str, Any]]:
        where, params = self._build_location_sql_filters(schema)
        where.append("UPPER(CPFCNPJ) LIKE UPPER(:busca_cpfcnpj)")
        params["busca_cpfcnpj"] = _varchar15_like_prefix(busca)
        self._append_exclude_ids(where, exclude_ids, params, "cpf")
        return self._fetch_rows_limited(where, params)

    def _fetch_rows_by_telefone(
        self,
        schema: PPessoaIndexSchema,
        busca: str,
        exclude_ids: set[int],
    ) -> list[dict[str, Any]]:
        where, params = self._build_location_sql_filters(schema)
        where.append("UPPER(TELEFONE) LIKE UPPER(:busca_telefone)")
        params["busca_telefone"] = _varchar15_like_prefix(busca)
        self._append_exclude_ids(where, exclude_ids, params, "tel")
        return self._fetch_rows_limited(where, params)

    def _fetch_rows_limited(
        self, where: list[str], params: dict[str, Any]
    ) -> list[dict[str, Any]]:
        where_sql = self._where_sql(where)
        sql = f"""
        SELECT FIRST {_BUSCA_BRANCH_LIMIT}
            {_SELECT_COLUMNS.strip()}
        FROM P_PESSOA
        {where_sql}
        ORDER BY PESSOA_ID DESC
        """
        rows = self.fetch_all(sql, params)
        return [map_pessoa_row(normalize_row_keys(row)) or {} for row in rows]

    @staticmethod
    def _append_exclude_ids(
        where: list[str],
        exclude_ids: set[int],
        params: dict[str, Any],
        prefix: str,
    ) -> None:
        if not exclude_ids:
            return
        placeholders: list[str] = []
        for index, pessoa_id in enumerate(sorted(exclude_ids)):
            key = f"ex_{prefix}_{index}"
            params[key] = pessoa_id
            placeholders.append(f":{key}")
        where.append(f"PESSOA_ID NOT IN ({', '.join(placeholders)})")

    def _build_location_sql_filters(
        self, schema: PPessoaIndexSchema, alias: str | None = None
    ) -> tuple[list[str], dict[str, Any]]:
        where: list[str] = []
        params: dict[str, Any] = {}
        prefix = f"{alias}." if alias else ""
        if schema.cidade is not None:
            where.append(f"UPPER(TRIM({prefix}CIDADE)) = UPPER(TRIM(:cidade))")
            params["cidade"] = schema.cidade
        if schema.uf is not None:
            where.append(f"UPPER(TRIM({prefix}UF)) = UPPER(TRIM(:uf))")
            params["uf"] = schema.uf
        self._append_tipo_pessoa_sql_filter(where, schema, alias)
        return where, params

    @staticmethod
    def _append_tipo_pessoa_sql_filter(
        where: list[str], schema: PPessoaIndexSchema, alias: str | None = None
    ) -> None:
        if schema.tipo_pessoa is None:
            return
        expected = _tipo_pessoa_digit_length(schema.tipo_pessoa)
        where.append(f"{_cpfcnpj_digits_length_sql(alias)} = {expected}")

    @staticmethod
    def _filter_rows_by_tipo_pessoa(
        rows: list[dict[str, Any]], schema: PPessoaIndexSchema
    ) -> list[dict[str, Any]]:
        if schema.tipo_pessoa is None:
            return rows
        return [
            row
            for row in rows
            if infer_tipo_pessoa_from_cpfcnpj(row.get("cpfcnpj"))
            == schema.tipo_pessoa
        ]

    @staticmethod
    def _cpfcnpj_group_key(row: dict[str, Any]) -> str | None:
        digits = _digits_only(str(row.get("cpfcnpj") or ""))
        return digits or None

    @classmethod
    def _group_rows_by_cpfcnpj(
        cls, rows: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        grouped: dict[str, dict[str, Any]] = {}
        ungrouped: list[dict[str, Any]] = []

        for row in rows:
            pessoa_id = row.get("pessoa_id")
            key = cls._cpfcnpj_group_key(row)
            if key is None or pessoa_id is None:
                ungrouped.append(row)
                continue

            current = grouped.get(key)
            if current is None or int(pessoa_id) > int(current.get("pessoa_id") or 0):
                grouped[key] = row

        return [*ungrouped, *grouped.values()]

    @staticmethod
    def _sort_rows(
        rows: list[dict[str, Any]], sort_field: str, sort_direction: str
    ) -> list[dict[str, Any]]:
        reverse = sort_direction.lower() == "desc"

        field_key = sort_field.lower()

        def sort_key(row: dict[str, Any]) -> Any:
            value = row.get(field_key)
            if value is None:
                return ""
            return value

        return sorted(rows, key=sort_key, reverse=reverse)

    def _execute_sql(
        self,
        pessoa_index_schema: PPessoaIndexSchema,
        page: int,
        per_page: int,
        sort_field: str,
        sort_direction: str,
    ) -> dict[str, Any]:
        grouped_ids_sql, params = self._grouped_pessoa_ids_sql(pessoa_index_schema)
        offset = (page - 1) * per_page

        count_sql = f"SELECT COUNT(*) AS TOTAL FROM ({grouped_ids_sql}) grouped"
        count_row = self.fetch_one(count_sql, params) or {}
        total = int(count_row.get("TOTAL") or count_row.get("total") or 0)

        sql = f"""
        SELECT FIRST {per_page} SKIP {offset}
            {_select_columns_sql("p")}
        FROM P_PESSOA p
        INNER JOIN ({grouped_ids_sql}) grouped ON grouped.PESSOA_ID = p.PESSOA_ID
        ORDER BY p.{sort_field} {sort_direction.upper()}
        """
        rows = self.fetch_all(sql, params)
        mapped_rows = [
            map_pessoa_row(normalize_row_keys(row)) or {} for row in rows
        ]

        return {
            "rows": self._enrich_rows_with_total_titulos(mapped_rows),
            "pagination": self._build_pagination_meta(page, per_page, total),
        }

    def _grouped_pessoa_ids_sql(
        self, schema: PPessoaIndexSchema
    ) -> tuple[str, dict[str, Any]]:
        non_empty_filters, params = self._build_sql_filters(schema, "pg")
        empty_filters, _ = self._build_sql_filters(schema, "pe")
        non_empty_doc = _normalized_cpfcnpj_sql("pg")
        empty_doc = _normalized_cpfcnpj_sql("pe")

        non_empty_where = self._where_sql([*non_empty_filters, f"{non_empty_doc} <> ''"])
        empty_where = self._where_sql([*empty_filters, f"{empty_doc} = ''"])
        sql = f"""
            SELECT MAX(pg.PESSOA_ID) AS PESSOA_ID
            FROM P_PESSOA pg
            {non_empty_where}
            GROUP BY {non_empty_doc}
            UNION ALL
            SELECT pe.PESSOA_ID AS PESSOA_ID
            FROM P_PESSOA pe
            {empty_where}
        """
        return sql, params

    def _enrich_rows_with_total_titulos(
        self, rows: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        pessoa_ids_by_doc = self._fetch_pessoa_ids_by_cpfcnpj_digits(
            sorted(
                {
                    self._cpfcnpj_group_key(row)
                    for row in rows
                    if self._cpfcnpj_group_key(row) is not None
                }
            )
        )

        pessoa_ids = [
            int(row["pessoa_id"])
            for row in rows
            if row.get("pessoa_id") is not None
        ]
        for grouped_ids in pessoa_ids_by_doc.values():
            pessoa_ids.extend(grouped_ids)

        counts = CountTitulosByPessoaIdsRepository().execute(pessoa_ids)
        for row in rows:
            pessoa_id = row.get("pessoa_id")
            cpfcnpj_key = self._cpfcnpj_group_key(row)
            if cpfcnpj_key is not None:
                row["total_titulos"] = sum(
                    counts.get(pessoa_group_id, 0)
                    for pessoa_group_id in pessoa_ids_by_doc.get(cpfcnpj_key, [])
                )
            else:
                row["total_titulos"] = (
                    counts.get(int(pessoa_id), 0) if pessoa_id is not None else 0
                )
        return rows

    def _fetch_pessoa_ids_by_cpfcnpj_digits(
        self, cpfcnpj_digits: list[str | None]
    ) -> dict[str, list[int]]:
        docs = [doc for doc in cpfcnpj_digits if doc]
        if not docs:
            return {}

        placeholders = ", ".join(f":doc_{index}" for index in range(len(docs)))
        params = {f"doc_{index}": doc for index, doc in enumerate(docs)}
        doc_expr = _normalized_cpfcnpj_sql()
        sql = f"""
        SELECT
            PESSOA_ID,
            {doc_expr} AS CPFCNPJ_DIGITS
        FROM P_PESSOA
        WHERE {doc_expr} IN ({placeholders})
        """
        rows = self.fetch_all(sql, params)
        grouped: dict[str, list[int]] = {doc: [] for doc in docs}
        for row in rows or []:
            pessoa_id = row.get("PESSOA_ID") or row.get("pessoa_id")
            doc = row.get("CPFCNPJ_DIGITS") or row.get("cpfcnpj_digits")
            if pessoa_id is None or not doc:
                continue
            grouped.setdefault(str(doc), []).append(int(pessoa_id))
        return grouped

    def _build_sql_filters(
        self, pessoa_index_schema: PPessoaIndexSchema, alias: str | None = None
    ) -> tuple[list[str], dict[str, Any]]:
        return self._build_location_sql_filters(pessoa_index_schema, alias)

    @staticmethod
    def _where_sql(where: list[str]) -> str:
        if not where:
            return ""
        return " WHERE " + " AND ".join(where)

    @staticmethod
    def _build_pagination_meta(page: int, per_page: int, total: int) -> dict[str, int]:
        total_pages = (total + per_page - 1) // per_page if per_page > 0 else 0
        return {
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": total_pages,
        }
