from __future__ import annotations

from datetime import datetime, timedelta
from decimal import Decimal
from typing import Any, Mapping, Optional

from orm_py import Op

from abstracts.repository import BaseRepository
from actions.data.query_params_parser import QueryParams, QueryParamsParser
from database.orm_firebird import normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_andamento import get_p_andamento_model
from packages.v1.administrativo.schemas.p_andamento_schema import (
    PAndamentoIndexSchema,
    _is_date_only,
    arquivo_gerado_from_db,
)

_PANDAMENTO_SORT_FIELD_MAP = {
    "andamento_id": "ANDAMENTO_ID",
    "ocorrencia_andamento_id": "OCORRENCIA_ANDAMENTO_ID",
    "data_ocorrencia": "DATA_OCORRENCIA",
    "titulo_id": "TITULO_ID",
    "usuario_id": "USUARIO_ID",
    "arquivo_gerado": "ARQUIVO_GERADO",
    "data_geracao": "DATA_GERACAO",
}

_SELECT_COLUMNS = """
    ANDAMENTO_ID,
    OCORRENCIA_ANDAMENTO_ID,
    DATA_OCORRENCIA,
    TITULO_ID,
    USUARIO_ID,
    ARQUIVO_GERADO,
    DATA_GERACAO
"""


class IndexRepository(BaseRepository):
    def execute(
        self,
        andamento_index_schema: PAndamentoIndexSchema,
        query_params: QueryParams,
    ) -> dict[str, Any]:
        page = query_params.page
        per_page = query_params.per_page
        sort_field, sort_direction = QueryParamsParser.resolve_sort(
            query_params,
            primary_key="andamento_id",
            field_map=_PANDAMENTO_SORT_FIELD_MAP,
        )

        if use_orm_firebird():
            return self._execute_orm(
                andamento_index_schema, page, per_page, sort_field, sort_direction
            )
        return self._execute_sql(
            andamento_index_schema, page, per_page, sort_field, sort_direction
        )

    def _execute_orm(
        self,
        andamento_index_schema: PAndamentoIndexSchema,
        page: int,
        per_page: int,
        sort_field: str,
        sort_direction: str,
    ) -> dict[str, Any]:
        where = self._build_orm_where(andamento_index_schema)
        offset = (page - 1) * per_page

        options: dict[str, Any] = {
            "order": [(sort_field, sort_direction.upper())],
            "limit": per_page,
            "offset": offset,
        }
        if where:
            options["where"] = where

        result = get_p_andamento_model().findAndCountAll(options)
        total = int(result.get("count") or 0)
        rows = result.get("rows") or []

        return {
            "rows": [self._map_andamento_row(row) or {} for row in rows],
            "pagination": self._build_pagination_meta(page, per_page, total),
        }

    def _execute_sql(
        self,
        andamento_index_schema: PAndamentoIndexSchema,
        page: int,
        per_page: int,
        sort_field: str,
        sort_direction: str,
    ) -> dict[str, Any]:
        where_clauses, params = self._build_sql_filters(andamento_index_schema)
        where_sql = self._where_sql(where_clauses)
        offset = (page - 1) * per_page

        count_sql = f"SELECT COUNT(*) AS TOTAL FROM P_ANDAMENTO{where_sql}"
        count_row = self.fetch_one(count_sql, params) or {}
        total = int(count_row.get("TOTAL") or count_row.get("total") or 0)

        sql = f"""
        SELECT FIRST {per_page} SKIP {offset}
            {_SELECT_COLUMNS.strip()}
        FROM P_ANDAMENTO
        {where_sql}
        ORDER BY {sort_field} {sort_direction.upper()}
        """
        rows = self.fetch_all(sql, params)

        return {
            "rows": [self._map_andamento_row(row) or {} for row in rows],
            "pagination": self._build_pagination_meta(page, per_page, total),
        }

    @staticmethod
    def _build_orm_where(andamento_index_schema: PAndamentoIndexSchema) -> dict[str, Any]:
        clauses: list[dict[str, Any]] = []

        if andamento_index_schema.titulo_id is not None:
            clauses.append({"TITULO_ID": andamento_index_schema.titulo_id})
        if andamento_index_schema.ocorrencia_andamento_id is not None:
            clauses.append(
                {
                    "OCORRENCIA_ANDAMENTO_ID": andamento_index_schema.ocorrencia_andamento_id
                }
            )
        if andamento_index_schema.data_ocorrencia is not None:
            clauses.append(
                IndexRepository._data_ocorrencia_orm_clause(
                    andamento_index_schema.data_ocorrencia
                )
            )

        if not clauses:
            return {}
        if len(clauses) == 1:
            return clauses[0]
        return {Op.and_: clauses}

    @staticmethod
    def _data_ocorrencia_orm_clause(value: datetime) -> dict[str, Any]:
        if _is_date_only(value):
            end = value + timedelta(days=1)
            return {
                Op.and_: [
                    {"DATA_OCORRENCIA": {Op.gte: value}},
                    {"DATA_OCORRENCIA": {Op.lt: end}},
                ]
            }
        return {"DATA_OCORRENCIA": value}

    def _build_sql_filters(
        self, andamento_index_schema: PAndamentoIndexSchema
    ) -> tuple[list[str], dict[str, Any]]:
        where: list[str] = []
        params: dict[str, Any] = {}

        if andamento_index_schema.titulo_id is not None:
            where.append("TITULO_ID = :titulo_id")
            params["titulo_id"] = andamento_index_schema.titulo_id
        if andamento_index_schema.ocorrencia_andamento_id is not None:
            where.append("OCORRENCIA_ANDAMENTO_ID = :ocorrencia_andamento_id")
            params["ocorrencia_andamento_id"] = (
                andamento_index_schema.ocorrencia_andamento_id
            )
        if andamento_index_schema.data_ocorrencia is not None:
            value = andamento_index_schema.data_ocorrencia
            if _is_date_only(value):
                where.append("CAST(DATA_OCORRENCIA AS DATE) = CAST(:data_ocorrencia AS DATE)")
                params["data_ocorrencia"] = value
            else:
                where.append("DATA_OCORRENCIA = :data_ocorrencia")
                params["data_ocorrencia"] = value

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
    def _map_andamento_row(row: Optional[Mapping[str, Any]]) -> Optional[dict[str, Any]]:
        mapped = normalize_row_keys(row)
        if mapped is None:
            return None

        for key in (
            "andamento_id",
            "ocorrencia_andamento_id",
            "titulo_id",
            "usuario_id",
        ):
            value = mapped.get(key)
            if isinstance(value, Decimal):
                mapped[key] = int(value)

        arquivo = mapped.get("arquivo_gerado")
        if arquivo is not None:
            mapped["arquivo_gerado"] = arquivo_gerado_from_db(str(arquivo))

        return mapped
