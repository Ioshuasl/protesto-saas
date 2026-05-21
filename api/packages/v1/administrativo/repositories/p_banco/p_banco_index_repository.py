from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from abstracts.repository import BaseRepository
from actions.data.query_params_parser import QueryParams, QueryParamsParser
from database.orm_firebird import normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_banco import get_p_banco_model
from packages.v1.administrativo.schemas.p_banco_schema import (
    PBancoIndexSchema,
    normalize_sim_nao_from_db,
)

_PBANCO_SORT_FIELD_MAP = {
    "banco_id": "BANCO_ID",
    "codigo_banco": "CODIGO_BANCO",
    "codigo": "CODIGO_BANCO",
    "descricao": "DESCRICAO",
    "pessoa_id": "PESSOA_ID",
    "layout_id": "LAYOUT_ID",
    "apontamento_pag_posterior": "APONTAMENTO_PAG_POSTERIOR",
    "custas_na_confirmacao": "CUSTAS_NA_CONFIRMACAO",
    "demais_despesas": "DEMAIS_DESPESAS",
}

_SELECT_COLUMNS = """
    BANCO_ID,
    CODIGO_BANCO,
    DESCRICAO,
    PESSOA_ID,
    LAYOUT_ID,
    APONTAMENTO_PAG_POSTERIOR,
    CUSTAS_NA_CONFIRMACAO,
    DEMAIS_DESPESAS
"""


class IndexRepository(BaseRepository):
    def execute(
        self,
        banco_index_schema: PBancoIndexSchema,
        query_params: QueryParams,
    ) -> dict[str, Any]:
        page = query_params.page
        per_page = query_params.per_page
        sort_field, sort_direction = QueryParamsParser.resolve_sort(
            query_params,
            primary_key="banco_id",
            field_map=_PBANCO_SORT_FIELD_MAP,
        )
        if use_orm_firebird() and not self._has_unified_search(banco_index_schema):
            return self._execute_orm(
                banco_index_schema, page, per_page, sort_field, sort_direction
            )
        return self._execute_sql(
            banco_index_schema, page, per_page, sort_field, sort_direction
        )

    def _execute_orm(
        self,
        banco_index_schema: PBancoIndexSchema,
        page: int,
        per_page: int,
        sort_field: str,
        sort_direction: str,
    ) -> dict[str, Any]:
        where = self._build_orm_where(banco_index_schema)
        offset = (page - 1) * per_page

        options: dict[str, Any] = {
            "order": [(sort_field, sort_direction.upper())],
            "limit": per_page,
            "offset": offset,
        }
        if where:
            options["where"] = where

        result = get_p_banco_model().findAndCountAll(options)
        total = int(result.get("count") or 0)
        rows = result.get("rows") or []

        return {
            "rows": [self._map_banco_row(row) or {} for row in rows],
            "pagination": self._build_pagination_meta(page, per_page, total),
        }

    def _execute_sql(
        self,
        banco_index_schema: PBancoIndexSchema,
        page: int,
        per_page: int,
        sort_field: str,
        sort_direction: str,
    ) -> dict[str, Any]:
        where_clauses, params = self._build_sql_filters(banco_index_schema)
        where_sql = self._where_sql(where_clauses)
        offset = (page - 1) * per_page

        count_sql = f"SELECT COUNT(*) AS TOTAL FROM P_BANCO{where_sql}"
        count_row = self.fetch_one(count_sql, params) or {}
        total = int(count_row.get("TOTAL") or count_row.get("total") or 0)

        sql = f"""
        SELECT FIRST {per_page} SKIP {offset}
            {_SELECT_COLUMNS.strip()}
        FROM P_BANCO
        {where_sql}
        ORDER BY {sort_field} {sort_direction.upper()}
        """
        rows = self.fetch_all(sql, params)

        return {
            "rows": [self._map_banco_row(row) or {} for row in rows],
            "pagination": self._build_pagination_meta(page, per_page, total),
        }

    @staticmethod
    def _has_unified_search(banco_index_schema: PBancoIndexSchema) -> bool:
        return banco_index_schema.busca is not None

    @staticmethod
    def _build_orm_where(banco_index_schema: PBancoIndexSchema) -> dict[str, Any]:
        return {}

    def _build_sql_filters(
        self, banco_index_schema: PBancoIndexSchema
    ) -> tuple[list[str], dict[str, Any]]:
        where: list[str] = []
        params: dict[str, Any] = {}

        if banco_index_schema.busca is not None:
            where.append(
                "(UPPER(CODIGO_BANCO) LIKE UPPER(:busca) OR UPPER(DESCRICAO) LIKE UPPER(:busca))"
            )
            params["busca"] = f"%{banco_index_schema.busca}%"

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
    def _map_banco_row(row: Optional[Mapping[str, Any]]) -> Optional[dict[str, Any]]:
        mapped = normalize_row_keys(row)
        if mapped is None:
            return None

        for key in ("banco_id", "pessoa_id", "layout_id"):
            value = mapped.get(key)
            if isinstance(value, Decimal):
                mapped[key] = int(value)

        demais = mapped.get("demais_despesas")
        if isinstance(demais, Decimal):
            mapped["demais_despesas"] = float(demais) if demais is not None else None
        if demais is None:
            mapped["demais_despesas"] = None

        mapped["apontamento_pag_posterior"] = normalize_sim_nao_from_db(
            mapped.get("apontamento_pag_posterior")
        )
        mapped["custas_na_confirmacao"] = normalize_sim_nao_from_db(
            mapped.get("custas_na_confirmacao")
        )

        codigo = mapped.get("codigo_banco")
        if codigo is not None:
            mapped["codigo_banco"] = str(codigo).strip() or None

        return mapped
