from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from abstracts.repository import BaseRepository
from actions.data.query_params_parser import QueryParams, QueryParamsParser
from database.orm_firebird import normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_livro_natureza import get_p_livro_natureza_model
from packages.v1.administrativo.schemas.p_livro_natureza_schema import (
    PLivroNaturezaIndexSchema,
    SIGLA_MAX_LENGTH,
    normalize_sigla_from_db,
    situacao_from_db,
)

_PLIVRO_NATUREZA_SORT_FIELD_MAP = {
    "livro_natureza_id": "LIVRO_NATUREZA_ID",
    "sigla": "SIGLA",
    "descricao": "DESCRICAO",
    "situacao": "SITUACAO",
}

_API_SORT_KEYS = {
    "LIVRO_NATUREZA_ID": "livro_natureza_id",
    "SIGLA": "sigla",
    "DESCRICAO": "descricao",
    "SITUACAO": "situacao",
}

_SELECT_COLUMNS = """
    LIVRO_NATUREZA_ID,
    SIGLA,
    DESCRICAO,
    SITUACAO
"""


class IndexRepository(BaseRepository):
    def execute(
        self,
        livro_natureza_index_schema: PLivroNaturezaIndexSchema,
        query_params: QueryParams,
    ) -> dict[str, Any]:
        page = query_params.page
        per_page = query_params.per_page
        sort_field, sort_direction = QueryParamsParser.resolve_sort(
            query_params,
            primary_key="livro_natureza_id",
            field_map=_PLIVRO_NATUREZA_SORT_FIELD_MAP,
        )

        if self._has_unified_search(livro_natureza_index_schema):
            return self._execute_busca_merged(
                livro_natureza_index_schema, page, per_page, sort_field, sort_direction
            )

        if use_orm_firebird():
            return self._execute_orm(
                livro_natureza_index_schema, page, per_page, sort_field, sort_direction
            )
        return self._execute_sql(
            livro_natureza_index_schema, page, per_page, sort_field, sort_direction
        )

    def _execute_busca_merged(
        self,
        livro_natureza_index_schema: PLivroNaturezaIndexSchema,
        page: int,
        per_page: int,
        sort_field: str,
        sort_direction: str,
    ) -> dict[str, Any]:
        term = str(livro_natureza_index_schema.busca or "").strip()
        merged: dict[int, dict[str, Any]] = {}

        if term:
            term_upper = term.upper()
            if len(term_upper) <= SIGLA_MAX_LENGTH:
                for row in self._fetch_by_sigla(term):
                    mapped = self._map_livro_natureza_row(row)
                    if mapped and mapped.get("livro_natureza_id") is not None:
                        merged[int(mapped["livro_natureza_id"])] = mapped

            for row in self._fetch_by_descricao(term):
                mapped = self._map_livro_natureza_row(row)
                if mapped and mapped.get("livro_natureza_id") is not None:
                    merged[int(mapped["livro_natureza_id"])] = mapped

        rows = self._sort_rows(list(merged.values()), sort_field, sort_direction)
        total = len(rows)
        offset = (page - 1) * per_page
        page_rows = rows[offset : offset + per_page]

        return {
            "rows": page_rows,
            "pagination": self._build_pagination_meta(page, per_page, total),
        }

    def _fetch_by_sigla(self, term: str) -> list[Mapping[str, Any]]:
        term_upper = term.upper()
        if not term_upper:
            return []

        sql = f"""
        SELECT {_SELECT_COLUMNS.strip()}
        FROM P_LIVRO_NATUREZA
        WHERE UPPER(TRIM(SIGLA)) = UPPER(:term_exact)
           OR UPPER(TRIM(SIGLA)) LIKE UPPER(:term_prefix)
        """
        term_exact = term_upper[:SIGLA_MAX_LENGTH]
        prefix_base = term_upper[: max(1, SIGLA_MAX_LENGTH - 1)]
        term_prefix = f"{prefix_base}%"

        return self.fetch_all(
            sql,
            {"term_exact": term_exact, "term_prefix": term_prefix},
        )

    def _fetch_by_descricao(self, term: str) -> list[Mapping[str, Any]]:
        sql = f"""
        SELECT {_SELECT_COLUMNS.strip()}
        FROM P_LIVRO_NATUREZA
        WHERE UPPER(DESCRICAO) LIKE UPPER(:busca_descricao)
        """
        return self.fetch_all(sql, {"busca_descricao": f"%{term}%"})

    @staticmethod
    def _sort_rows(
        rows: list[dict[str, Any]],
        sort_field: str,
        sort_direction: str,
    ) -> list[dict[str, Any]]:
        api_key = _API_SORT_KEYS.get(sort_field, "livro_natureza_id")
        reverse = sort_direction.upper() == "DESC"

        def sort_key(row: dict[str, Any]):
            value = row.get(api_key)
            if value is None:
                return (1, "")
            if api_key == "livro_natureza_id":
                return (0, int(value))
            return (0, str(value).upper())

        return sorted(rows, key=sort_key, reverse=reverse)

    def _execute_orm(
        self,
        livro_natureza_index_schema: PLivroNaturezaIndexSchema,
        page: int,
        per_page: int,
        sort_field: str,
        sort_direction: str,
    ) -> dict[str, Any]:
        offset = (page - 1) * per_page
        options: dict[str, Any] = {
            "order": [(sort_field, sort_direction.upper())],
            "limit": per_page,
            "offset": offset,
        }
        result = get_p_livro_natureza_model().findAndCountAll(options)
        total = int(result.get("count") or 0)
        rows = result.get("rows") or []
        return {
            "rows": [self._map_livro_natureza_row(row) or {} for row in rows],
            "pagination": self._build_pagination_meta(page, per_page, total),
        }

    def _execute_sql(
        self,
        livro_natureza_index_schema: PLivroNaturezaIndexSchema,
        page: int,
        per_page: int,
        sort_field: str,
        sort_direction: str,
    ) -> dict[str, Any]:
        offset = (page - 1) * per_page

        count_sql = "SELECT COUNT(*) AS TOTAL FROM P_LIVRO_NATUREZA"
        count_row = self.fetch_one(count_sql, {}) or {}
        total = int(count_row.get("TOTAL") or count_row.get("total") or 0)

        sql = f"""
        SELECT FIRST {per_page} SKIP {offset}
            {_SELECT_COLUMNS.strip()}
        FROM P_LIVRO_NATUREZA
        ORDER BY {sort_field} {sort_direction.upper()}
        """
        rows = self.fetch_all(sql, {})
        return {
            "rows": [self._map_livro_natureza_row(row) or {} for row in rows],
            "pagination": self._build_pagination_meta(page, per_page, total),
        }

    @staticmethod
    def _has_unified_search(
        livro_natureza_index_schema: PLivroNaturezaIndexSchema,
    ) -> bool:
        return livro_natureza_index_schema.busca is not None

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
    def _map_livro_natureza_row(
        row: Optional[Mapping[str, Any]],
    ) -> Optional[dict[str, Any]]:
        mapped = normalize_row_keys(row)
        if mapped is None:
            return None

        livro_natureza_id = mapped.get("livro_natureza_id")
        if isinstance(livro_natureza_id, Decimal):
            mapped["livro_natureza_id"] = int(livro_natureza_id)

        mapped["sigla"] = normalize_sigla_from_db(mapped.get("sigla"))

        descricao = mapped.get("descricao")
        if descricao is not None:
            mapped["descricao"] = str(descricao).strip() or None

        mapped["situacao"] = situacao_from_db(mapped.get("situacao"))
        mapped.pop("tipo", None)
        mapped.pop("natureza_id", None)

        return mapped
