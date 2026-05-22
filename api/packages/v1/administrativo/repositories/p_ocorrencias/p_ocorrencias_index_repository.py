from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from orm_py import Op

from abstracts.repository import BaseRepository
from actions.data.query_params_parser import QueryParams, QueryParamsParser
from database.orm_firebird import firebird_orm_supports_string_where, normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_ocorrencias import get_p_ocorrencias_model
from packages.v1.administrativo.repositories.p_ocorrencias.p_ocorrencias_count_titulos_by_ocorrencias_ids_repository import (
    CountTitulosByOcorrenciasIdsRepository,
)
from packages.v1.administrativo.schemas.p_ocorrencias_schema import (
    POcorrenciasIndexSchema,
    tipo_from_db,
)

_POCORRENCIAS_SORT_FIELD_MAP = {
    "ocorrencias_id": "OCORRENCIAS_ID",
    "codigo": "CODIGO",
    "descricao": "DESCRICAO",
    "tipo": "TIPO",
}

_SELECT_COLUMNS = """
    OCORRENCIAS_ID,
    CODIGO,
    DESCRICAO,
    TIPO
"""


class IndexRepository(BaseRepository):
    def execute(
        self,
        ocorrencias_index_schema: POcorrenciasIndexSchema,
        query_params: QueryParams,
    ) -> dict[str, Any]:
        page = query_params.page
        per_page = query_params.per_page
        sort_field, sort_direction = QueryParamsParser.resolve_sort(
            query_params,
            primary_key="ocorrencias_id",
            field_map=_POCORRENCIAS_SORT_FIELD_MAP,
        )

        if use_orm_firebird() and (
            firebird_orm_supports_string_where()
            or not self._has_string_filters(ocorrencias_index_schema)
        ):
            return self._execute_orm(
                ocorrencias_index_schema, page, per_page, sort_field, sort_direction
            )
        return self._execute_sql(
            ocorrencias_index_schema, page, per_page, sort_field, sort_direction
        )

    def _execute_orm(
        self,
        ocorrencias_index_schema: POcorrenciasIndexSchema,
        page: int,
        per_page: int,
        sort_field: str,
        sort_direction: str,
    ) -> dict[str, Any]:
        where = self._build_orm_where(ocorrencias_index_schema)
        offset = (page - 1) * per_page

        options: dict[str, Any] = {
            "order": [(sort_field, sort_direction.upper())],
            "limit": per_page,
            "offset": offset,
        }
        if where:
            options["where"] = where

        result = get_p_ocorrencias_model().findAndCountAll(options)
        total = int(result.get("count") or 0)
        rows = result.get("rows") or []

        mapped_rows = [self._map_ocorrencias_row(row) or {} for row in rows]
        return {
            "rows": self._enrich_rows_with_total_titulos(mapped_rows),
            "pagination": self._build_pagination_meta(page, per_page, total),
        }

    def _execute_sql(
        self,
        ocorrencias_index_schema: POcorrenciasIndexSchema,
        page: int,
        per_page: int,
        sort_field: str,
        sort_direction: str,
    ) -> dict[str, Any]:
        where_clauses, params = self._build_sql_filters(ocorrencias_index_schema)
        where_sql = self._where_sql(where_clauses)
        offset = (page - 1) * per_page

        count_sql = f"SELECT COUNT(*) AS TOTAL FROM P_OCORRENCIAS{where_sql}"
        count_row = self.fetch_one(count_sql, params) or {}
        total = int(count_row.get("TOTAL") or count_row.get("total") or 0)

        sql = f"""
        SELECT FIRST {per_page} SKIP {offset}
            {_SELECT_COLUMNS.strip()}
        FROM P_OCORRENCIAS
        {where_sql}
        ORDER BY {sort_field} {sort_direction.upper()}
        """
        rows = self.fetch_all(sql, params)

        mapped_rows = [self._map_ocorrencias_row(row) or {} for row in rows]
        return {
            "rows": self._enrich_rows_with_total_titulos(mapped_rows),
            "pagination": self._build_pagination_meta(page, per_page, total),
        }

    def _enrich_rows_with_total_titulos(
        self, rows: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        ocorrencias_ids = [
            int(row["ocorrencias_id"])
            for row in rows
            if row.get("ocorrencias_id") is not None
        ]
        counts = CountTitulosByOcorrenciasIdsRepository().execute(ocorrencias_ids)
        for row in rows:
            ocorrencias_id = row.get("ocorrencias_id")
            row["total_titulos"] = (
                counts.get(int(ocorrencias_id), 0)
                if ocorrencias_id is not None
                else 0
            )
        return rows

    @staticmethod
    def _has_string_filters(ocorrencias_index_schema: POcorrenciasIndexSchema) -> bool:
        return (
            ocorrencias_index_schema.busca is not None
            or ocorrencias_index_schema.tipo is not None
        )

    @staticmethod
    def _build_orm_where(
        ocorrencias_index_schema: POcorrenciasIndexSchema,
    ) -> dict[str, Any]:
        clauses: list[dict[str, Any]] = []

        if ocorrencias_index_schema.busca is not None:
            term = f"%{ocorrencias_index_schema.busca}%"
            clauses.append(
                {
                    Op.or_: [
                        {"DESCRICAO": {Op.like: term}},
                        {"CODIGO": {Op.like: term}},
                    ]
                }
            )
        if ocorrencias_index_schema.tipo is not None:
            clauses.append({"TIPO": ocorrencias_index_schema.tipo})

        if not clauses:
            return {}
        if len(clauses) == 1:
            return clauses[0]
        return {Op.and_: clauses}

    def _build_sql_filters(
        self, ocorrencias_index_schema: POcorrenciasIndexSchema
    ) -> tuple[list[str], dict[str, Any]]:
        where: list[str] = []
        params: dict[str, Any] = {}

        if ocorrencias_index_schema.busca is not None:
            where.append(
                "(UPPER(DESCRICAO) LIKE UPPER(:busca) OR UPPER(CODIGO) LIKE UPPER(:busca))"
            )
            params["busca"] = f"%{ocorrencias_index_schema.busca}%"
        if ocorrencias_index_schema.tipo is not None:
            where.append("UPPER(TRIM(TIPO)) = UPPER(TRIM(:tipo))")
            params["tipo"] = ocorrencias_index_schema.tipo

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
    def _map_ocorrencias_row(
        row: Optional[Mapping[str, Any]],
    ) -> Optional[dict[str, Any]]:
        mapped = normalize_row_keys(row)
        if mapped is None:
            return None

        ocorrencias_id = mapped.get("ocorrencias_id")
        if isinstance(ocorrencias_id, Decimal):
            mapped["ocorrencias_id"] = int(ocorrencias_id)

        codigo = mapped.get("codigo")
        if codigo is not None:
            mapped["codigo"] = str(codigo).strip() or None

        descricao = mapped.get("descricao")
        if descricao is not None:
            mapped["descricao"] = str(descricao).strip() or None

        mapped["tipo"] = tipo_from_db(mapped.get("tipo"))
        return mapped
