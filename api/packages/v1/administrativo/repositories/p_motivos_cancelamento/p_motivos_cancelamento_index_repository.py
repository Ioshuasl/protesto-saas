from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from orm_py import Op

from abstracts.repository import BaseRepository
from actions.data.query_params_parser import QueryParams, QueryParamsParser
from database.orm_firebird import firebird_orm_supports_string_where, normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_motivos_cancelamento import (
    get_p_motivos_cancelamento_model,
)
from packages.v1.administrativo.repositories.p_motivos_cancelamento.p_motivos_cancelamento_count_titulos_by_ids_repository import (
    CountTitulosByMotivosCancelamentoIdsRepository,
)
from packages.v1.administrativo.schemas.p_motivos_cancelamento_schema import (
    PMotivosCancelamentoIndexSchema,
    situacao_from_db,
)

_PMOTIVOS_CANCELAMENTO_SORT_FIELD_MAP = {
    "motivos_cancelamento_id": "MOTIVOS_CANCELAMENTO_ID",
    "descricao": "DESCRICAO",
    "situacao": "SITUACAO",
}

_SELECT_COLUMNS = """
    MOTIVOS_CANCELAMENTO_ID,
    DESCRICAO,
    SITUACAO
"""


class IndexRepository(BaseRepository):
    def execute(
        self,
        motivos_cancelamento_index_schema: PMotivosCancelamentoIndexSchema,
        query_params: QueryParams,
    ) -> dict[str, Any]:
        page = query_params.page
        per_page = query_params.per_page
        sort_field, sort_direction = QueryParamsParser.resolve_sort(
            query_params,
            primary_key="motivos_cancelamento_id",
            field_map=_PMOTIVOS_CANCELAMENTO_SORT_FIELD_MAP,
        )

        if use_orm_firebird() and (
            firebird_orm_supports_string_where()
            or not self._has_string_filters(motivos_cancelamento_index_schema)
        ):
            return self._execute_orm(
                motivos_cancelamento_index_schema,
                page,
                per_page,
                sort_field,
                sort_direction,
            )
        return self._execute_sql(
            motivos_cancelamento_index_schema,
            page,
            per_page,
            sort_field,
            sort_direction,
        )

    def _execute_orm(
        self,
        motivos_cancelamento_index_schema: PMotivosCancelamentoIndexSchema,
        page: int,
        per_page: int,
        sort_field: str,
        sort_direction: str,
    ) -> dict[str, Any]:
        where = self._build_orm_where(motivos_cancelamento_index_schema)
        offset = (page - 1) * per_page

        options: dict[str, Any] = {
            "order": [(sort_field, sort_direction.upper())],
            "limit": per_page,
            "offset": offset,
        }
        if where:
            options["where"] = where

        result = get_p_motivos_cancelamento_model().findAndCountAll(options)
        total = int(result.get("count") or 0)
        rows = result.get("rows") or []

        mapped_rows = [self._map_row(row) or {} for row in rows]
        return {
            "rows": self._enrich_rows_with_total_titulos(mapped_rows),
            "pagination": self._build_pagination_meta(page, per_page, total),
        }

    def _execute_sql(
        self,
        motivos_cancelamento_index_schema: PMotivosCancelamentoIndexSchema,
        page: int,
        per_page: int,
        sort_field: str,
        sort_direction: str,
    ) -> dict[str, Any]:
        where_clauses, params = self._build_sql_filters(motivos_cancelamento_index_schema)
        where_sql = self._where_sql(where_clauses)
        offset = (page - 1) * per_page

        count_sql = f"SELECT COUNT(*) AS TOTAL FROM P_MOTIVOS_CANCELAMENTO{where_sql}"
        count_row = self.fetch_one(count_sql, params) or {}
        total = int(count_row.get("TOTAL") or count_row.get("total") or 0)

        sql = f"""
        SELECT FIRST {per_page} SKIP {offset}
            {_SELECT_COLUMNS.strip()}
        FROM P_MOTIVOS_CANCELAMENTO
        {where_sql}
        ORDER BY {sort_field} {sort_direction.upper()}
        """
        rows = self.fetch_all(sql, params)

        mapped_rows = [self._map_row(row) or {} for row in rows]
        return {
            "rows": self._enrich_rows_with_total_titulos(mapped_rows),
            "pagination": self._build_pagination_meta(page, per_page, total),
        }

    def _enrich_rows_with_total_titulos(
        self, rows: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        ids = [
            int(row["motivos_cancelamento_id"])
            for row in rows
            if row.get("motivos_cancelamento_id") is not None
        ]
        counts = CountTitulosByMotivosCancelamentoIdsRepository().execute(ids)
        for row in rows:
            pk = row.get("motivos_cancelamento_id")
            row["total_titulos"] = (
                counts.get(int(pk), 0) if pk is not None else 0
            )
        return rows

    @staticmethod
    def _has_string_filters(
        motivos_cancelamento_index_schema: PMotivosCancelamentoIndexSchema,
    ) -> bool:
        return motivos_cancelamento_index_schema.descricao is not None

    @staticmethod
    def _build_orm_where(
        motivos_cancelamento_index_schema: PMotivosCancelamentoIndexSchema,
    ) -> dict[str, Any]:
        if motivos_cancelamento_index_schema.descricao is None:
            return {}
        return {
            "DESCRICAO": {
                Op.like: f"%{motivos_cancelamento_index_schema.descricao}%"
            }
        }

    def _build_sql_filters(
        self,
        motivos_cancelamento_index_schema: PMotivosCancelamentoIndexSchema,
    ) -> tuple[list[str], dict[str, Any]]:
        where: list[str] = []
        params: dict[str, Any] = {}

        if motivos_cancelamento_index_schema.descricao is not None:
            where.append("UPPER(DESCRICAO) LIKE UPPER(:descricao)")
            params["descricao"] = f"%{motivos_cancelamento_index_schema.descricao}%"

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

        pk = mapped.get("motivos_cancelamento_id")
        if isinstance(pk, Decimal):
            mapped["motivos_cancelamento_id"] = int(pk)

        descricao = mapped.get("descricao")
        if descricao is not None:
            mapped["descricao"] = str(descricao).strip() or None

        mapped["situacao"] = situacao_from_db(mapped.get("situacao"))
        return mapped
