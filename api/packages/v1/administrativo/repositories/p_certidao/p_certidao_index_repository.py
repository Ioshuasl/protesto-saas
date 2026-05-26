from __future__ import annotations

from datetime import timedelta
from decimal import Decimal, InvalidOperation
from typing import Any, Mapping, Optional

from orm_py import Op

from abstracts.repository import BaseRepository
from actions.data.query_params_parser import QueryParams, QueryParamsParser
from database.orm_firebird import firebird_orm_supports_string_where, normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_certidao import get_p_certidao_model
from packages.v1.administrativo.schemas.p_certidao_schema import PCertidaoIndexSchema

_PCERTIDAO_SORT_FIELD_MAP = {
    "certidao_id": "CERTIDAO_ID",
    "data_certidao": "DATA_CERTIDAO",
    "tipo_certidao": "TIPO_CERTIDAO",
    "status": "STATUS",
    "cpfcnpj": "CPFCNPJ",
    "nome": "NOME",
}

_SELECT_COLUMNS = """
    CERTIDAO_ID,
    USUARIO_ID,
    DATA_CERTIDAO,
    HORA_CERTIDAO,
    TIPO_CERTIDAO,
    VALOR_EMOLUMENTO,
    VALOR_TAXA_JUDICIARIA,
    VALOR_FUNDESP,
    VALOR_TAXA_EXTRA,
    NUMERO_IMPRESSAO,
    CPFCNPJ,
    NOME,
    STATUS,
    OBSERVACAO,
    VALOR_TAXA_ISS,
    APRESENTANTE,
    NFSE_ID,
    QTD_PROTESTOS,
    QTD_CANCELADOS,
    QTD_SUSTADO,
    N_REMESSA,
    TIPO_REMESSA,
    PROTECAO_CREDITO_ID
"""

_INDEX_SELECT_COLUMNS = """
    P_CERTIDAO.CERTIDAO_ID,
    P_CERTIDAO.USUARIO_ID,
    P_CERTIDAO.DATA_CERTIDAO,
    P_CERTIDAO.HORA_CERTIDAO,
    P_CERTIDAO.TIPO_CERTIDAO,
    P_CERTIDAO.VALOR_EMOLUMENTO,
    P_CERTIDAO.VALOR_TAXA_JUDICIARIA,
    P_CERTIDAO.VALOR_FUNDESP,
    P_CERTIDAO.VALOR_TAXA_EXTRA,
    P_CERTIDAO.NUMERO_IMPRESSAO,
    P_CERTIDAO.CPFCNPJ,
    P_CERTIDAO.NOME,
    P_CERTIDAO.STATUS,
    P_CERTIDAO.OBSERVACAO,
    P_CERTIDAO.VALOR_TAXA_ISS,
    P_CERTIDAO.APRESENTANTE,
    P_CERTIDAO.NFSE_ID,
    P_CERTIDAO.QTD_PROTESTOS,
    P_CERTIDAO.QTD_CANCELADOS,
    P_CERTIDAO.QTD_SUSTADO,
    P_CERTIDAO.N_REMESSA,
    P_CERTIDAO.TIPO_REMESSA,
    P_CERTIDAO.PROTECAO_CREDITO_ID
"""

_INTEGER_FIELDS = {
    "certidao_id",
    "usuario_id",
    "numero_impressao",
    "nfse_id",
    "qtd_protestos",
    "qtd_cancelados",
    "qtd_sustado",
    "n_remessa",
    "protecao_credito_id",
}

_MONEY_FIELDS = {
    "valor_emolumento",
    "valor_taxa_judiciaria",
    "valor_fundesp",
    "valor_taxa_extra",
    "valor_taxa_iss",
}

_TEXT_FIELDS = {
    "hora_certidao",
    "tipo_certidao",
    "cpfcnpj",
    "nome",
    "status",
    "apresentante",
    "tipo_remessa",
    "usuario_nome",
}

_PCERTIDAO_INDEX_INCLUDES: list[dict[str, Any]] = [
    {
        "association": "usuario",
        "required": False,
        "attributes": ["USUARIO_ID", "NOME_COMPLETO", "LOGIN"],
    }
]

_INDEX_TIPOS_CERTIDAO = ("P", "N")


class IndexRepository(BaseRepository):
    def execute(
        self,
        certidao_index_schema: PCertidaoIndexSchema,
        query_params: QueryParams,
    ) -> dict[str, Any]:
        page = query_params.page
        per_page = query_params.per_page
        sort_field, sort_direction = QueryParamsParser.resolve_sort(
            query_params,
            primary_key="certidao_id",
            field_map=_PCERTIDAO_SORT_FIELD_MAP,
        )

        if use_orm_firebird() and (
            firebird_orm_supports_string_where()
            or not self._has_string_filters(certidao_index_schema)
        ):
            return self._execute_orm(
                certidao_index_schema, page, per_page, sort_field, sort_direction
            )
        return self._execute_sql(
            certidao_index_schema, page, per_page, sort_field, sort_direction
        )

    def _execute_orm(
        self,
        certidao_index_schema: PCertidaoIndexSchema,
        page: int,
        per_page: int,
        sort_field: str,
        sort_direction: str,
    ) -> dict[str, Any]:
        where = self._build_orm_where(certidao_index_schema)
        offset = (page - 1) * per_page

        options: dict[str, Any] = {
            "order": [(sort_field, sort_direction.upper())],
            "limit": per_page,
            "offset": offset,
            "include": _PCERTIDAO_INDEX_INCLUDES,
        }
        if where:
            options["where"] = where

        result = get_p_certidao_model().findAndCountAll(options)
        total = int(result.get("count") or 0)
        rows = result.get("rows") or []

        return {
            "rows": [self._map_row(row) or {} for row in rows],
            "pagination": self._build_pagination_meta(page, per_page, total),
        }

    def _execute_sql(
        self,
        certidao_index_schema: PCertidaoIndexSchema,
        page: int,
        per_page: int,
        sort_field: str,
        sort_direction: str,
    ) -> dict[str, Any]:
        where_clauses, params = self._build_sql_filters(certidao_index_schema)
        where_sql = self._where_sql(where_clauses)
        offset = (page - 1) * per_page

        count_sql = f"SELECT COUNT(*) AS TOTAL FROM P_CERTIDAO{where_sql}"
        count_row = self.fetch_one(count_sql, params) or {}
        total = int(count_row.get("TOTAL") or count_row.get("total") or 0)

        sql = f"""
        SELECT FIRST {per_page} SKIP {offset}
            {_INDEX_SELECT_COLUMNS.strip()},
            COALESCE(NULLIF(TRIM(U.NOME_COMPLETO), ''), U.LOGIN) AS USUARIO_NOME
        FROM P_CERTIDAO
        LEFT JOIN G_USUARIO U ON U.USUARIO_ID = P_CERTIDAO.USUARIO_ID
        {where_sql}
        ORDER BY {sort_field} {sort_direction.upper()}
        """
        rows = self.fetch_all(sql, params)

        return {
            "rows": [self._map_row(row) or {} for row in rows],
            "pagination": self._build_pagination_meta(page, per_page, total),
        }

    @staticmethod
    def _has_string_filters(certidao_index_schema: PCertidaoIndexSchema) -> bool:
        return any(
            [
                certidao_index_schema.tipo_certidao is not None,
                certidao_index_schema.status is not None,
                certidao_index_schema.busca is not None,
            ]
        )

    @staticmethod
    def _build_orm_where(certidao_index_schema: PCertidaoIndexSchema) -> dict[str, Any]:
        clauses: list[dict[str, Any]] = [
            {"TIPO_CERTIDAO": {Op.in_: list(_INDEX_TIPOS_CERTIDAO)}}
        ]

        if certidao_index_schema.tipo_certidao is not None:
            clauses.append({"TIPO_CERTIDAO": certidao_index_schema.tipo_certidao})
        if certidao_index_schema.data_certidao is not None:
            clauses.append(
                IndexRepository._date_range_orm_clause(
                    certidao_index_schema.data_certidao,
                    certidao_index_schema.data_certidao,
                )
            )
        else:
            if certidao_index_schema.data_inicio is not None:
                clauses.append(
                    {"DATA_CERTIDAO": {Op.gte: certidao_index_schema.data_inicio}}
                )
            if certidao_index_schema.data_fim is not None:
                clauses.append(
                    {"DATA_CERTIDAO": {Op.lt: certidao_index_schema.data_fim + timedelta(days=1)}}
                )
        if certidao_index_schema.status is not None:
            clauses.append({"STATUS": certidao_index_schema.status})
        if certidao_index_schema.busca is not None:
            term = f"%{certidao_index_schema.busca}%"
            clauses.append(
                {
                    Op.or_: [
                        {"CPFCNPJ": {Op.like: term}},
                        {"NOME": {Op.like: term}},
                    ]
                }
            )

        if not clauses:
            return {}
        if len(clauses) == 1:
            return clauses[0]
        return {Op.and_: clauses}

    @staticmethod
    def _date_range_orm_clause(data_inicio: Any, data_fim: Any) -> dict[str, Any]:
        return {
            Op.and_: [
                {"DATA_CERTIDAO": {Op.gte: data_inicio}},
                {"DATA_CERTIDAO": {Op.lt: data_fim + timedelta(days=1)}},
            ]
        }

    def _build_sql_filters(
        self, certidao_index_schema: PCertidaoIndexSchema
    ) -> tuple[list[str], dict[str, Any]]:
        where: list[str] = ["UPPER(TRIM(TIPO_CERTIDAO)) IN ('P', 'N')"]
        params: dict[str, Any] = {}

        if certidao_index_schema.tipo_certidao is not None:
            where.append("UPPER(TRIM(TIPO_CERTIDAO)) = UPPER(:tipo_certidao)")
            params["tipo_certidao"] = certidao_index_schema.tipo_certidao
        if certidao_index_schema.data_certidao is not None:
            where.append("CAST(DATA_CERTIDAO AS DATE) = :data_certidao")
            params["data_certidao"] = certidao_index_schema.data_certidao
        else:
            if certidao_index_schema.data_inicio is not None:
                where.append("CAST(DATA_CERTIDAO AS DATE) >= :data_inicio")
                params["data_inicio"] = certidao_index_schema.data_inicio
            if certidao_index_schema.data_fim is not None:
                where.append("CAST(DATA_CERTIDAO AS DATE) <= :data_fim")
                params["data_fim"] = certidao_index_schema.data_fim
        if certidao_index_schema.status is not None:
            where.append("UPPER(TRIM(STATUS)) = UPPER(:status)")
            params["status"] = certidao_index_schema.status
        if certidao_index_schema.busca is not None:
            where.append("(UPPER(CPFCNPJ) LIKE UPPER(:busca) OR UPPER(NOME) LIKE UPPER(:busca))")
            params["busca"] = f"%{certidao_index_schema.busca}%"

        return where, params

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

    @staticmethod
    def _blob_to_text(value: Any) -> Optional[str]:
        if value is None:
            return None
        if isinstance(value, str):
            return value.strip() or None
        if isinstance(value, (bytes, bytearray)):
            for encoding in ("utf-8", "latin-1"):
                try:
                    return bytes(value).decode(encoding).strip() or None
                except UnicodeDecodeError:
                    continue
            return None
        return str(value).strip() or None

    @classmethod
    def _map_row(cls, row: Optional[Mapping[str, Any]]) -> Optional[dict[str, Any]]:
        mapped = normalize_row_keys(row)
        if mapped is None:
            return None

        usuario = cls._mapping_or_empty(mapped.get("usuario"))
        usuario_nome = usuario.get("NOME_COMPLETO") or usuario.get("nome_completo")
        usuario_login = usuario.get("LOGIN") or usuario.get("login")
        if mapped.get("usuario_nome") is None:
            mapped["usuario_nome"] = usuario_nome or usuario_login

        for key in _INTEGER_FIELDS:
            value = mapped.get(key)
            mapped[key] = cls._int_or_original(value)

        for key in _MONEY_FIELDS:
            value = mapped.get(key)
            mapped[key] = cls._float_or_original(value)

        for key in _TEXT_FIELDS:
            value = mapped.get(key)
            if value is not None:
                mapped[key] = str(value).strip() or None

        mapped["observacao"] = cls._blob_to_text(mapped.get("observacao"))
        mapped.pop("usuario", None)
        return mapped

    @staticmethod
    def _mapping_or_empty(value: Any) -> dict[str, Any]:
        if isinstance(value, Mapping):
            return dict(value)
        return {}

    @staticmethod
    def _int_or_original(value: Any) -> Any:
        if value is None:
            return None
        if isinstance(value, Decimal):
            return int(value)
        if isinstance(value, str):
            try:
                decimal_value = Decimal(value)
            except (InvalidOperation, ValueError):
                return value
            if decimal_value == decimal_value.to_integral_value():
                return int(decimal_value)
        return value

    @staticmethod
    def _float_or_original(value: Any) -> Any:
        if value is None:
            return None
        if isinstance(value, Decimal):
            return float(value)
        if isinstance(value, str):
            try:
                return float(Decimal(value))
            except (InvalidOperation, ValueError):
                return value
        return value
