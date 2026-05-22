from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from orm_py import Op

from abstracts.repository import BaseRepository
from actions.data.query_params_parser import QueryParams, QueryParamsParser
from database.orm_firebird import firebird_orm_supports_string_where, normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_motivos import get_p_motivos_model
from packages.v1.administrativo.repositories.p_motivos.p_motivos_count_titulos_by_motivos_ids_repository import (
    CountTitulosByMotivosIdsRepository,
)
from packages.v1.administrativo.schemas.p_motivos_schema import (
    PMotivosIndexSchema,
    SITUACAO_CODIGO_ATIVO,
    SITUACAO_CODIGO_INATIVO,
    situacao_from_db,
)

_PMOTIVOS_SORT_FIELD_MAP = {
    "motivos_id": "MOTIVOS_ID",
    "codigo": "CODIGO",
    "descricao": "DESCRICAO",
    "situacao": "SITUACAO",
}

_SELECT_COLUMNS = """
    MOTIVOS_ID,
    DESCRICAO,
    SITUACAO,
    CODIGO
"""


class IndexRepository(BaseRepository):
    def execute(
        self,
        motivos_index_schema: PMotivosIndexSchema,
        query_params: QueryParams,
    ) -> dict[str, Any]:
        page = query_params.page
        per_page = query_params.per_page
        sort_field, sort_direction = QueryParamsParser.resolve_sort(
            query_params,
            primary_key="motivos_id",
            field_map=_PMOTIVOS_SORT_FIELD_MAP,
        )

        if use_orm_firebird() and (
            firebird_orm_supports_string_where()
            or not self._has_string_filters(motivos_index_schema)
        ):
            return self._execute_orm(
                motivos_index_schema, page, per_page, sort_field, sort_direction
            )
        return self._execute_sql(
            motivos_index_schema, page, per_page, sort_field, sort_direction
        )

    def _execute_orm(
        self,
        motivos_index_schema: PMotivosIndexSchema,
        page: int,
        per_page: int,
        sort_field: str,
        sort_direction: str,
    ) -> dict[str, Any]:
        where = self._build_orm_where(motivos_index_schema)
        offset = (page - 1) * per_page

        options: dict[str, Any] = {
            "order": [(sort_field, sort_direction.upper())],
            "limit": per_page,
            "offset": offset,
        }
        if where:
            options["where"] = where

        result = get_p_motivos_model().findAndCountAll(options)
        total = int(result.get("count") or 0)
        rows = result.get("rows") or []

        mapped_rows = [self._map_motivos_row(row) or {} for row in rows]
        return {
            "rows": self._enrich_rows_with_total_titulos(mapped_rows),
            "pagination": self._build_pagination_meta(page, per_page, total),
        }

    def _execute_sql(
        self,
        motivos_index_schema: PMotivosIndexSchema,
        page: int,
        per_page: int,
        sort_field: str,
        sort_direction: str,
    ) -> dict[str, Any]:
        where_clauses, params = self._build_sql_filters(motivos_index_schema)
        where_sql = self._where_sql(where_clauses)
        offset = (page - 1) * per_page

        count_sql = f"SELECT COUNT(*) AS TOTAL FROM P_MOTIVOS{where_sql}"
        count_row = self.fetch_one(count_sql, params) or {}
        total = int(count_row.get("TOTAL") or count_row.get("total") or 0)

        sql = f"""
        SELECT FIRST {per_page} SKIP {offset}
            {_SELECT_COLUMNS.strip()}
        FROM P_MOTIVOS
        {where_sql}
        ORDER BY {sort_field} {sort_direction.upper()}
        """
        rows = self.fetch_all(sql, params)

        mapped_rows = [self._map_motivos_row(row) or {} for row in rows]
        return {
            "rows": self._enrich_rows_with_total_titulos(mapped_rows),
            "pagination": self._build_pagination_meta(page, per_page, total),
        }

    def _enrich_rows_with_total_titulos(
        self, rows: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        motivos_ids = [
            int(row["motivos_id"])
            for row in rows
            if row.get("motivos_id") is not None
        ]
        counts = CountTitulosByMotivosIdsRepository().execute(motivos_ids)
        for row in rows:
            motivos_id = row.get("motivos_id")
            row["total_titulos"] = (
                counts.get(int(motivos_id), 0) if motivos_id is not None else 0
            )
        return rows

    @staticmethod
    def _has_string_filters(motivos_index_schema: PMotivosIndexSchema) -> bool:
        return (
            motivos_index_schema.descricao is not None
            or motivos_index_schema.situacao is not None
        )

    @staticmethod
    def _build_orm_where(motivos_index_schema: PMotivosIndexSchema) -> dict[str, Any]:
        clauses: list[dict[str, Any]] = []

        if motivos_index_schema.descricao is not None:
            clauses.append(
                {"DESCRICAO": {Op.like: f"%{motivos_index_schema.descricao}%"}}
            )
        if motivos_index_schema.situacao == SITUACAO_CODIGO_ATIVO:
            clauses.append({"SITUACAO": SITUACAO_CODIGO_ATIVO})
        elif motivos_index_schema.situacao == SITUACAO_CODIGO_INATIVO:
            clauses.append(
                {
                    Op.or_: [
                        {"SITUACAO": {Op.is_: None}},
                        {"SITUACAO": ""},
                        {"SITUACAO": SITUACAO_CODIGO_INATIVO},
                    ]
                }
            )

        if not clauses:
            return {}
        if len(clauses) == 1:
            return clauses[0]
        return {Op.and_: clauses}

    @staticmethod
    def _append_situacao_filter(
        where: list[str], params: dict[str, Any], situacao: str
    ) -> None:
        code = (situacao or "").strip().upper()
        if code == SITUACAO_CODIGO_ATIVO:
            where.append("UPPER(TRIM(SITUACAO)) = 'A'")
        elif code == SITUACAO_CODIGO_INATIVO:
            where.append(
                "(SITUACAO IS NULL OR TRIM(COALESCE(SITUACAO, '')) = '' "
                "OR UPPER(TRIM(SITUACAO)) = 'I')"
            )
        params.pop("situacao", None)

    def _build_sql_filters(
        self, motivos_index_schema: PMotivosIndexSchema
    ) -> tuple[list[str], dict[str, Any]]:
        where: list[str] = []
        params: dict[str, Any] = motivos_index_schema.model_dump(exclude_none=True)

        if motivos_index_schema.descricao is not None:
            where.append("UPPER(DESCRICAO) LIKE UPPER(:descricao)")
            params["descricao"] = f"%{motivos_index_schema.descricao}%"
        if motivos_index_schema.situacao is not None:
            self._append_situacao_filter(where, params, motivos_index_schema.situacao)

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
    def _map_motivos_row(row: Optional[Mapping[str, Any]]) -> Optional[dict[str, Any]]:
        mapped = normalize_row_keys(row)
        if mapped is None:
            return None

        motivos_id = mapped.get("motivos_id")
        if isinstance(motivos_id, Decimal):
            mapped["motivos_id"] = int(motivos_id)

        codigo = mapped.get("codigo")
        if codigo is not None:
            mapped["codigo"] = str(codigo).strip() or None

        descricao = mapped.get("descricao")
        if descricao is not None:
            mapped["descricao"] = str(descricao).strip() or None

        mapped["situacao"] = situacao_from_db(mapped.get("situacao"))
        return mapped
