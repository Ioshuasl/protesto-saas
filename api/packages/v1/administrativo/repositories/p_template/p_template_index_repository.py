from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from orm_py import Op

from abstracts.repository import BaseRepository
from actions.data.query_params_parser import QueryParams, QueryParamsParser
from database.orm_firebird import firebird_orm_supports_string_where, normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_template import get_p_template_model
from packages.v1.administrativo.schemas.p_template_schema import PTemplateIndexSchema

_PTEMPLATE_SORT_FIELD_MAP = {
    "template_id": "TEMPLATE_ID",
    "descricao": "DESCRICAO",
}

_SELECT_COLUMNS = """
    TEMPLATE_ID,
    DESCRICAO
"""

_SELECT_ATTRIBUTES = ["TEMPLATE_ID", "DESCRICAO"]


class IndexRepository(BaseRepository):
    def execute(
        self,
        template_index_schema: PTemplateIndexSchema,
        query_params: QueryParams,
    ) -> dict[str, Any]:
        page = query_params.page
        per_page = query_params.per_page
        sort_field, sort_direction = QueryParamsParser.resolve_sort(
            query_params,
            primary_key="template_id",
            field_map=_PTEMPLATE_SORT_FIELD_MAP,
        )

        if use_orm_firebird() and (
            firebird_orm_supports_string_where()
            or not self._has_string_filters(template_index_schema)
        ):
            return self._execute_orm(
                template_index_schema, page, per_page, sort_field, sort_direction
            )
        return self._execute_sql(
            template_index_schema, page, per_page, sort_field, sort_direction
        )

    def _execute_orm(
        self,
        template_index_schema: PTemplateIndexSchema,
        page: int,
        per_page: int,
        sort_field: str,
        sort_direction: str,
    ) -> dict[str, Any]:
        where = self._build_orm_where(template_index_schema)
        offset = (page - 1) * per_page

        options: dict[str, Any] = {
            "attributes": _SELECT_ATTRIBUTES,
            "order": [(sort_field, sort_direction.upper())],
            "limit": per_page,
            "offset": offset,
        }
        if where:
            options["where"] = where

        result = get_p_template_model().findAndCountAll(options)
        total = int(result.get("count") or 0)
        rows = result.get("rows") or []

        return {
            "rows": [self._map_row(row) or {} for row in rows],
            "pagination": self._build_pagination_meta(page, per_page, total),
        }

    def _execute_sql(
        self,
        template_index_schema: PTemplateIndexSchema,
        page: int,
        per_page: int,
        sort_field: str,
        sort_direction: str,
    ) -> dict[str, Any]:
        where_clauses, params = self._build_sql_filters(template_index_schema)
        where_sql = self._where_sql(where_clauses)
        offset = (page - 1) * per_page

        count_sql = f"SELECT COUNT(*) AS TOTAL FROM P_TEMPLATE{where_sql}"
        count_row = self.fetch_one(count_sql, params) or {}
        total = int(count_row.get("TOTAL") or count_row.get("total") or 0)

        sql = f"""
        SELECT FIRST {per_page} SKIP {offset}
            {_SELECT_COLUMNS.strip()}
        FROM P_TEMPLATE
        {where_sql}
        ORDER BY {sort_field} {sort_direction.upper()}
        """
        rows = self.fetch_all(sql, params)

        return {
            "rows": [self._map_row(row) or {} for row in rows],
            "pagination": self._build_pagination_meta(page, per_page, total),
        }

    @staticmethod
    def _has_string_filters(template_index_schema: PTemplateIndexSchema) -> bool:
        return template_index_schema.descricao is not None

    @staticmethod
    def _build_orm_where(template_index_schema: PTemplateIndexSchema) -> dict[str, Any]:
        clauses: list[dict[str, Any]] = []

        if template_index_schema.template_id is not None:
            clauses.append({"TEMPLATE_ID": template_index_schema.template_id})
        if template_index_schema.descricao is not None:
            clauses.append({"DESCRICAO": {Op.like: f"%{template_index_schema.descricao}%"}})

        if not clauses:
            return {}
        if len(clauses) == 1:
            return clauses[0]
        return {Op.and_: clauses}

    @staticmethod
    def _build_sql_filters(
        template_index_schema: PTemplateIndexSchema,
    ) -> tuple[list[str], dict[str, Any]]:
        where: list[str] = []
        params = template_index_schema.model_dump(exclude_none=True)

        if template_index_schema.template_id is not None:
            where.append("TEMPLATE_ID = :template_id")
        if template_index_schema.descricao is not None:
            where.append("UPPER(DESCRICAO) LIKE UPPER(:descricao)")
            params["descricao"] = f"%{template_index_schema.descricao}%"

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

        template_id = mapped.get("template_id")
        if isinstance(template_id, Decimal):
            mapped["template_id"] = int(template_id)

        descricao = mapped.get("descricao")
        if descricao is not None:
            mapped["descricao"] = str(descricao).strip()

        return {
            "template_id": mapped.get("template_id"),
            "descricao": mapped.get("descricao"),
        }
