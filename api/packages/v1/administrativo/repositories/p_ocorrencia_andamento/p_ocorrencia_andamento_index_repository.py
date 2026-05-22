from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from orm_py import Op

from abstracts.repository import BaseRepository
from actions.data.query_params_parser import QueryParams, QueryParamsParser
from database.orm_firebird import firebird_orm_supports_string_where, normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_ocorrencia_andamento import (
    get_p_ocorrencia_andamento_model,
)
from packages.v1.administrativo.schemas.p_ocorrencia_andamento_schema import (
    POcorrenciaAndamentoIndexSchema,
)

_POCORRENCIA_ANDAMENTO_SORT_FIELD_MAP = {
    "ocorrencia_andamento_id": "OCORRENCIA_ANDAMENTO_ID",
    "codigo": "CODIGO",
    "descricao": "DESCRICAO",
}

_SELECT_COLUMNS = """
    OCORRENCIA_ANDAMENTO_ID,
    CODIGO,
    DESCRICAO
"""


class IndexRepository(BaseRepository):
    def execute(
        self,
        ocorrencia_andamento_index_schema: POcorrenciaAndamentoIndexSchema,
        query_params: QueryParams,
    ) -> dict[str, Any]:
        page = query_params.page
        per_page = query_params.per_page
        sort_field, sort_direction = QueryParamsParser.resolve_sort(
            query_params,
            primary_key="ocorrencia_andamento_id",
            field_map=_POCORRENCIA_ANDAMENTO_SORT_FIELD_MAP,
        )

        if use_orm_firebird() and (
            firebird_orm_supports_string_where()
            or not self._has_string_filters(ocorrencia_andamento_index_schema)
        ):
            return self._execute_orm(
                ocorrencia_andamento_index_schema,
                page,
                per_page,
                sort_field,
                sort_direction,
            )
        return self._execute_sql(
            ocorrencia_andamento_index_schema,
            page,
            per_page,
            sort_field,
            sort_direction,
        )

    def _execute_orm(
        self,
        ocorrencia_andamento_index_schema: POcorrenciaAndamentoIndexSchema,
        page: int,
        per_page: int,
        sort_field: str,
        sort_direction: str,
    ) -> dict[str, Any]:
        where = self._build_orm_where(ocorrencia_andamento_index_schema)
        offset = (page - 1) * per_page

        options: dict[str, Any] = {
            "order": [(sort_field, sort_direction.upper())],
            "limit": per_page,
            "offset": offset,
        }
        if where:
            options["where"] = where

        result = get_p_ocorrencia_andamento_model().findAndCountAll(options)
        total = int(result.get("count") or 0)
        rows = result.get("rows") or []

        return {
            "rows": [self._map_row(row) or {} for row in rows],
            "pagination": self._build_pagination_meta(page, per_page, total),
        }

    def _execute_sql(
        self,
        ocorrencia_andamento_index_schema: POcorrenciaAndamentoIndexSchema,
        page: int,
        per_page: int,
        sort_field: str,
        sort_direction: str,
    ) -> dict[str, Any]:
        where_clauses, params = self._build_sql_filters(ocorrencia_andamento_index_schema)
        where_sql = self._where_sql(where_clauses)
        offset = (page - 1) * per_page

        count_sql = f"SELECT COUNT(*) AS TOTAL FROM P_OCORRENCIA_ANDAMENTO{where_sql}"
        count_row = self.fetch_one(count_sql, params) or {}
        total = int(count_row.get("TOTAL") or count_row.get("total") or 0)

        sql = f"""
        SELECT FIRST {per_page} SKIP {offset}
            {_SELECT_COLUMNS.strip()}
        FROM P_OCORRENCIA_ANDAMENTO
        {where_sql}
        ORDER BY {sort_field} {sort_direction.upper()}
        """
        rows = self.fetch_all(sql, params)

        return {
            "rows": [self._map_row(row) or {} for row in rows],
            "pagination": self._build_pagination_meta(page, per_page, total),
        }

    @staticmethod
    def _has_string_filters(
        ocorrencia_andamento_index_schema: POcorrenciaAndamentoIndexSchema,
    ) -> bool:
        return ocorrencia_andamento_index_schema.descricao is not None

    @staticmethod
    def _build_orm_where(
        ocorrencia_andamento_index_schema: POcorrenciaAndamentoIndexSchema,
    ) -> dict[str, Any]:
        if ocorrencia_andamento_index_schema.descricao is None:
            return {}
        return {
            "DESCRICAO": {
                Op.like: f"%{ocorrencia_andamento_index_schema.descricao}%"
            }
        }

    def _build_sql_filters(
        self, ocorrencia_andamento_index_schema: POcorrenciaAndamentoIndexSchema
    ) -> tuple[list[str], dict[str, Any]]:
        where: list[str] = []
        params: dict[str, Any] = {}

        if ocorrencia_andamento_index_schema.descricao is not None:
            where.append("UPPER(DESCRICAO) LIKE UPPER(:descricao)")
            params["descricao"] = f"%{ocorrencia_andamento_index_schema.descricao}%"

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
    def _map_row(row: Optional[Mapping[str, Any]]) -> Optional[dict[str, Any]]:
        mapped = normalize_row_keys(row)
        if mapped is None:
            return None

        ocorrencia_andamento_id = mapped.get("ocorrencia_andamento_id")
        if isinstance(ocorrencia_andamento_id, Decimal):
            mapped["ocorrencia_andamento_id"] = int(ocorrencia_andamento_id)

        codigo = mapped.get("codigo")
        if codigo is not None:
            mapped["codigo"] = str(codigo).strip().upper() or None

        descricao = mapped.get("descricao")
        if descricao is not None:
            mapped["descricao"] = str(descricao).strip() or None

        return mapped
