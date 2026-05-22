from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from orm_py import Op

from abstracts.repository import BaseRepository
from actions.data.query_params_parser import QueryParams, QueryParamsParser
from database.orm_firebird import firebird_orm_supports_string_where, normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.g_feriado import get_g_feriado_model
from packages.v1.administrativo.schemas.g_feriado_schema import GFeriadoIndexSchema

SITUACAO_CODIGO_ATIVO = "A"
SITUACAO_CODIGO_INATIVO = "I"

_GFERIADO_SORT_FIELD_MAP = {
    "feriado_id": "FERIADO_ID",
    "ano": "ANO",
    "mes": "MES",
    "dia": "DIA",
    "data": "DATA",
    "descricao": "DESCRICAO",
    "tipo": "TIPO",
    "situacao": "SITUACAO",
}

_SELECT_COLUMNS = """
    FERIADO_ID,
    ANO,
    MES,
    DIA,
    DATA,
    DESCRICAO,
    TIPO,
    SITUACAO
"""


class IndexRepository(BaseRepository):
    def execute(
        self,
        feriado_index_schema: GFeriadoIndexSchema,
        query_params: QueryParams,
    ) -> dict[str, Any]:
        page = query_params.page
        per_page = query_params.per_page
        sort_field, sort_direction = QueryParamsParser.resolve_sort(
            query_params,
            primary_key="feriado_id",
            field_map=_GFERIADO_SORT_FIELD_MAP,
        )

        if use_orm_firebird() and (
            firebird_orm_supports_string_where()
            or not self._has_string_filters(feriado_index_schema)
        ):
            return self._execute_orm(
                feriado_index_schema, page, per_page, sort_field, sort_direction
            )
        return self._execute_sql(
            feriado_index_schema, page, per_page, sort_field, sort_direction
        )

    def _execute_orm(
        self,
        feriado_index_schema: GFeriadoIndexSchema,
        page: int,
        per_page: int,
        sort_field: str,
        sort_direction: str,
    ) -> dict[str, Any]:
        where = self._build_orm_where(feriado_index_schema)
        offset = (page - 1) * per_page

        options: dict[str, Any] = {
            "order": [(sort_field, sort_direction.upper())],
            "limit": per_page,
            "offset": offset,
        }
        if where:
            options["where"] = where

        result = get_g_feriado_model().findAndCountAll(options)
        total = int(result.get("count") or 0)
        rows = result.get("rows") or []

        return {
            "rows": [self._map_feriado_row(row) or {} for row in rows],
            "pagination": self._build_pagination_meta(page, per_page, total),
        }

    def _execute_sql(
        self,
        feriado_index_schema: GFeriadoIndexSchema,
        page: int,
        per_page: int,
        sort_field: str,
        sort_direction: str,
    ) -> dict[str, Any]:
        where_clauses, params = self._build_sql_filters(feriado_index_schema)
        where_sql = self._where_sql(where_clauses)
        offset = (page - 1) * per_page

        count_sql = f"SELECT COUNT(*) AS TOTAL FROM G_FERIADO{where_sql}"
        count_row = self.fetch_one(count_sql, params) or {}
        total = int(count_row.get("TOTAL") or count_row.get("total") or 0)

        sql = f"""
        SELECT FIRST {per_page} SKIP {offset}
            {_SELECT_COLUMNS.strip()}
        FROM G_FERIADO
        {where_sql}
        ORDER BY {sort_field} {sort_direction.upper()}
        """
        rows = self.fetch_all(sql, params)

        return {
            "rows": [self._map_feriado_row(row) or {} for row in rows],
            "pagination": self._build_pagination_meta(page, per_page, total),
        }

    @staticmethod
    def _has_string_filters(feriado_index_schema: GFeriadoIndexSchema) -> bool:
        return any(
            [
                feriado_index_schema.tipo is not None,
                feriado_index_schema.situacao is not None,
                feriado_index_schema.descricao is not None,
            ]
        )

    @staticmethod
    def _build_orm_where(feriado_index_schema: GFeriadoIndexSchema) -> dict[str, Any]:
        clauses: list[dict[str, Any]] = []

        if feriado_index_schema.ano is not None:
            clauses.append({"ANO": feriado_index_schema.ano})
        if feriado_index_schema.tipo is not None:
            clauses.append({"TIPO": feriado_index_schema.tipo})
        if feriado_index_schema.situacao == SITUACAO_CODIGO_ATIVO:
            clauses.append({"SITUACAO": SITUACAO_CODIGO_ATIVO})
        elif feriado_index_schema.situacao == SITUACAO_CODIGO_INATIVO:
            clauses.append(
                {
                    Op.or_: [
                        {"SITUACAO": {Op.is_: None}},
                        {"SITUACAO": ""},
                        {"SITUACAO": SITUACAO_CODIGO_INATIVO},
                    ]
                }
            )
        if feriado_index_schema.descricao is not None:
            clauses.append(
                {"DESCRICAO": {Op.like: f"%{feriado_index_schema.descricao}%"}}
            )

        if not clauses:
            return {}
        if len(clauses) == 1:
            return clauses[0]
        return {Op.and_: clauses}

    def _build_sql_filters(
        self, feriado_index_schema: GFeriadoIndexSchema
    ) -> tuple[list[str], dict[str, Any]]:
        where: list[str] = []
        params = feriado_index_schema.model_dump(exclude_none=True)

        if feriado_index_schema.ano is not None:
            where.append("ANO = :ano")
        if feriado_index_schema.tipo is not None:
            where.append("UPPER(TIPO) = UPPER(:tipo)")
        if feriado_index_schema.situacao is not None:
            self._append_situacao_filter(where, params, feriado_index_schema.situacao)
        if feriado_index_schema.descricao is not None:
            where.append("UPPER(DESCRICAO) LIKE UPPER(:descricao)")
            params["descricao"] = f"%{feriado_index_schema.descricao}%"

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

    @staticmethod
    def _map_feriado_row(row: Optional[Mapping[str, Any]]) -> Optional[dict[str, Any]]:
        mapped = normalize_row_keys(row)
        if mapped is None:
            return None

        feriado_id = mapped.get("feriado_id")
        if isinstance(feriado_id, Decimal):
            mapped["feriado_id"] = int(feriado_id)

        for key in ("ano", "mes", "dia"):
            value = mapped.get(key)
            if isinstance(value, Decimal):
                mapped[key] = int(value)

        tipo = mapped.get("tipo")
        if tipo is not None:
            mapped["tipo"] = str(tipo).strip().upper() or None

        situacao = mapped.get("situacao")
        if situacao is None or not str(situacao).strip():
            mapped["situacao"] = SITUACAO_CODIGO_INATIVO
        else:
            mapped["situacao"] = str(situacao).strip().upper()

        return mapped
