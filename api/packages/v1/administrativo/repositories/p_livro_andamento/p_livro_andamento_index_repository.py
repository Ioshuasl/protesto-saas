from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from orm_py import Op

from abstracts.repository import BaseRepository
from actions.data.query_params_parser import QueryParams, QueryParamsParser
from database.orm_firebird import normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_livro_andamento import get_p_livro_andamento_model
from packages.v1.administrativo.schemas.p_livro_andamento_schema import (
    PLivroAndamentoIndexSchema,
    is_livro_aberto,
    normalize_sigla,
)

_PLIVRO_ANDAMENTO_SORT_FIELD_MAP = {
    "livro_andamento_id": "LIVRO_ANDAMENTO_ID",
    "livro_natureza_id": "LIVRO_NATUREZA_ID",
    "folha_atual": "FOLHA_ATUAL",
    "numero_livro": "NUMERO_LIVRO",
    "data_abertura": "DATA_ABERTURA",
    "data_fechamento": "DATA_FECHAMENTO",
    "numero_folhas": "NUMERO_FOLHAS",
    "sigla": "SIGLA",
    "usuario_id": "USUARIO_ID",
}

_SELECT_COLUMNS = """
    LIVRO_ANDAMENTO_ID,
    LIVRO_NATUREZA_ID,
    FOLHA_ATUAL,
    NUMERO_LIVRO,
    DATA_ABERTURA,
    DATA_FECHAMENTO,
    NUMERO_FOLHAS,
    SIGLA,
    USUARIO_ID
"""


class IndexRepository(BaseRepository):
    def execute(
        self,
        livro_andamento_index_schema: PLivroAndamentoIndexSchema,
        query_params: QueryParams,
    ) -> dict[str, Any]:
        page = query_params.page
        per_page = query_params.per_page
        sort_field, sort_direction = QueryParamsParser.resolve_sort(
            query_params,
            primary_key="data_abertura",
            field_map=_PLIVRO_ANDAMENTO_SORT_FIELD_MAP,
        )

        if use_orm_firebird():
            return self._execute_orm(
                livro_andamento_index_schema,
                page,
                per_page,
                sort_field,
                sort_direction,
            )
        if self._has_unified_search(livro_andamento_index_schema):
            return self._execute_busca_merged(
                livro_andamento_index_schema,
                page,
                per_page,
                sort_field,
                sort_direction,
            )
        return self._execute_sql(
            livro_andamento_index_schema,
            page,
            per_page,
            sort_field,
            sort_direction,
        )

    def _execute_busca_merged(
        self,
        livro_andamento_index_schema: PLivroAndamentoIndexSchema,
        page: int,
        per_page: int,
        sort_field: str,
        sort_direction: str,
    ) -> dict[str, Any]:
        term = str(livro_andamento_index_schema.busca or "").strip()
        merged: dict[int, dict[str, Any]] = {}
        base_where, base_params = self._build_filter_clause(livro_andamento_index_schema)

        if term:
            for row in self._fetch_by_sigla(term, base_where, base_params):
                mapped = self._map_livro_andamento_row(row)
                if mapped and mapped.get("livro_andamento_id") is not None:
                    merged[int(mapped["livro_andamento_id"])] = mapped

            if term.isdigit():
                for row in self._fetch_by_numero_livro(int(term), base_where, base_params):
                    mapped = self._map_livro_andamento_row(row)
                    if mapped and mapped.get("livro_andamento_id") is not None:
                        merged[int(mapped["livro_andamento_id"])] = mapped

        rows = self._sort_rows(list(merged.values()), sort_field, sort_direction)
        total = len(rows)
        offset = (page - 1) * per_page
        page_rows = rows[offset : offset + per_page]

        return {
            "rows": page_rows,
            "pagination": self._build_pagination_meta(page, per_page, total),
        }

    def _fetch_by_sigla(
        self, term: str, base_where: str, base_params: dict[str, Any]
    ) -> list[Mapping[str, Any]]:
        term_upper = term.upper()[:3]
        if not term_upper:
            return []
        where = f"{base_where} AND UPPER(TRIM(SIGLA)) LIKE UPPER(:term_sigla)"
        params = {**base_params, "term_sigla": f"%{term_upper}%"}
        sql = f"SELECT {_SELECT_COLUMNS.strip()} FROM P_LIVRO_ANDAMENTO WHERE {where}"
        return self.fetch_all(sql, params)

    def _fetch_by_numero_livro(
        self, numero: int, base_where: str, base_params: dict[str, Any]
    ) -> list[Mapping[str, Any]]:
        where = f"{base_where} AND NUMERO_LIVRO = :numero_livro"
        params = {**base_params, "numero_livro": numero}
        sql = f"SELECT {_SELECT_COLUMNS.strip()} FROM P_LIVRO_ANDAMENTO WHERE {where}"
        return self.fetch_all(sql, params)

    @staticmethod
    def _sort_rows(
        rows: list[dict[str, Any]],
        sort_field: str,
        sort_direction: str,
    ) -> list[dict[str, Any]]:
        reverse = sort_direction.upper() == "DESC"
        field_map = {v: k for k, v in _PLIVRO_ANDAMENTO_SORT_FIELD_MAP.items()}
        api_key = field_map.get(sort_field, "data_abertura")

        def sort_key(row: dict[str, Any]):
            value = row.get(api_key)
            if value is None:
                return (1, "")
            if api_key in ("livro_andamento_id", "livro_natureza_id", "numero_livro", "folha_atual", "numero_folhas", "usuario_id"):
                return (0, int(value))
            if api_key in ("data_abertura", "data_fechamento"):
                return (0, str(value))
            return (0, str(value).upper())

        return sorted(rows, key=sort_key, reverse=reverse)

    def _execute_orm(
        self,
        livro_andamento_index_schema: PLivroAndamentoIndexSchema,
        page: int,
        per_page: int,
        sort_field: str,
        sort_direction: str,
    ) -> dict[str, Any]:
        where = self._build_orm_where(livro_andamento_index_schema)
        offset = (page - 1) * per_page
        options: dict[str, Any] = {
            "order": [(sort_field, sort_direction.upper())],
            "limit": per_page,
            "offset": offset,
        }
        if where:
            options["where"] = where
        result = get_p_livro_andamento_model().findAndCountAll(options)
        total = int(result.get("count") or 0)
        rows = result.get("rows") or []
        return {
            "rows": [self._map_livro_andamento_row(row) or {} for row in rows],
            "pagination": self._build_pagination_meta(page, per_page, total),
        }

    def _execute_sql(
        self,
        livro_andamento_index_schema: PLivroAndamentoIndexSchema,
        page: int,
        per_page: int,
        sort_field: str,
        sort_direction: str,
    ) -> dict[str, Any]:
        offset = (page - 1) * per_page
        where_clause, params = self._build_filter_clause(livro_andamento_index_schema)
        where_sql = f"WHERE {where_clause}" if where_clause else ""

        count_sql = f"SELECT COUNT(*) AS TOTAL FROM P_LIVRO_ANDAMENTO {where_sql}"
        count_row = self.fetch_one(count_sql, params) or {}
        total = int(count_row.get("TOTAL") or count_row.get("total") or 0)

        sql = f"""
        SELECT FIRST {per_page} SKIP {offset}
            {_SELECT_COLUMNS.strip()}
        FROM P_LIVRO_ANDAMENTO
        {where_sql}
        ORDER BY {sort_field} {sort_direction.upper()}
        """
        rows = self.fetch_all(sql, params)
        return {
            "rows": [self._map_livro_andamento_row(row) or {} for row in rows],
            "pagination": self._build_pagination_meta(page, per_page, total),
        }

    @staticmethod
    def _build_orm_where(
        livro_andamento_index_schema: PLivroAndamentoIndexSchema,
    ) -> dict[str, Any]:
        clauses: list[dict[str, Any]] = []

        if livro_andamento_index_schema.livro_natureza_id is not None:
            clauses.append(
                {
                    "LIVRO_NATUREZA_ID": livro_andamento_index_schema.livro_natureza_id
                }
            )
        if livro_andamento_index_schema.aberto == "S":
            clauses.append({"DATA_FECHAMENTO": {Op.is_: None}})
        elif livro_andamento_index_schema.aberto == "N":
            clauses.append({"DATA_FECHAMENTO": {Op.not_: None}})

        if livro_andamento_index_schema.busca is not None:
            term = str(livro_andamento_index_schema.busca).strip()
            if term:
                busca_clauses: list[dict[str, Any]] = [
                    {"SIGLA": {Op.like: f"%{term.upper()[:3]}%"}},
                ]
                if term.isdigit():
                    busca_clauses.append({"NUMERO_LIVRO": int(term)})
                clauses.append({Op.or_: busca_clauses})

        if not clauses:
            return {}
        if len(clauses) == 1:
            return clauses[0]
        return {Op.and_: clauses}

    @staticmethod
    def _has_unified_search(
        livro_andamento_index_schema: PLivroAndamentoIndexSchema,
    ) -> bool:
        return livro_andamento_index_schema.busca is not None

    def _build_filter_clause(
        self, livro_andamento_index_schema: PLivroAndamentoIndexSchema
    ) -> tuple[str, dict[str, Any]]:
        parts: list[str] = ["1=1"]
        params: dict[str, Any] = {}

        if livro_andamento_index_schema.livro_natureza_id is not None:
            parts.append("LIVRO_NATUREZA_ID = :livro_natureza_id")
            params["livro_natureza_id"] = livro_andamento_index_schema.livro_natureza_id

        if livro_andamento_index_schema.aberto == "S":
            parts.append("DATA_FECHAMENTO IS NULL")
        elif livro_andamento_index_schema.aberto == "N":
            parts.append("DATA_FECHAMENTO IS NOT NULL")

        return " AND ".join(parts), params

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
    def _map_livro_andamento_row(
        row: Optional[Mapping[str, Any]],
    ) -> Optional[dict[str, Any]]:
        mapped = normalize_row_keys(row)
        if mapped is None:
            return None

        for key in (
            "livro_andamento_id",
            "livro_natureza_id",
            "folha_atual",
            "numero_livro",
            "numero_folhas",
            "usuario_id",
        ):
            val = mapped.get(key)
            if isinstance(val, Decimal):
                mapped[key] = int(val)

        sigla = mapped.get("sigla")
        if sigla is not None:
            mapped["sigla"] = normalize_sigla(str(sigla))

        mapped["aberto"] = is_livro_aberto(mapped.get("data_fechamento"))
        return mapped
