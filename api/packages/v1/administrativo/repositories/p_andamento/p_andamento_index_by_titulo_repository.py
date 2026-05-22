from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from abstracts.repository import BaseRepository
from actions.data.query_params_parser import QueryParams, QueryParamsParser
from database.orm_firebird import normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_andamento import get_p_andamento_model
from packages.v1.administrativo.repositories.p_andamento.p_andamento_index_repository import (
    IndexRepository,
    _PANDAMENTO_SORT_FIELD_MAP,
)
from packages.v1.administrativo.schemas.p_andamento_schema import (
    PAndamentoIndexByTituloSchema,
    PAndamentoIndexSchema,
    arquivo_gerado_from_db,
)

_OCORRENCIA_ANDAMENTO_INCLUDE = [
    {
        "association": "ocorrencia_andamento",
        "required": False,
        "attributes": ["OCORRENCIA_ANDAMENTO_ID", "CODIGO", "DESCRICAO"],
    }
]

_SELECT_JOIN_COLUMNS = """
    PA.ANDAMENTO_ID,
    PA.OCORRENCIA_ANDAMENTO_ID,
    PA.DATA_OCORRENCIA,
    PA.TITULO_ID,
    PA.USUARIO_ID,
    PA.ARQUIVO_GERADO,
    PA.DATA_GERACAO,
    POA.CODIGO AS OCA_CODIGO,
    POA.DESCRICAO AS OCA_DESCRICAO
"""


class IndexByTituloRepository(BaseRepository):
    def execute(
        self,
        titulo_id: int,
        filter_schema: PAndamentoIndexByTituloSchema,
        query_params: QueryParams,
    ) -> dict[str, Any]:
        page = query_params.page
        per_page = query_params.per_page
        sort_field, sort_direction = QueryParamsParser.resolve_sort(
            query_params,
            primary_key="andamento_id",
            field_map=_PANDAMENTO_SORT_FIELD_MAP,
        )

        index_filters = PAndamentoIndexSchema(
            titulo_id=titulo_id,
            data_ocorrencia=filter_schema.data_ocorrencia,
            ocorrencia_andamento_id=filter_schema.ocorrencia_andamento_id,
        )

        if use_orm_firebird():
            return self._execute_orm(
                index_filters, page, per_page, sort_field, sort_direction
            )
        return self._execute_sql(
            index_filters, page, per_page, sort_field, sort_direction
        )

    def _execute_orm(
        self,
        index_filters: PAndamentoIndexSchema,
        page: int,
        per_page: int,
        sort_field: str,
        sort_direction: str,
    ) -> dict[str, Any]:
        where = IndexRepository._build_orm_where(index_filters)
        offset = (page - 1) * per_page

        options: dict[str, Any] = {
            "where": where or {"TITULO_ID": index_filters.titulo_id},
            "order": [(sort_field, sort_direction.upper())],
            "limit": per_page,
            "offset": offset,
            "include": _OCORRENCIA_ANDAMENTO_INCLUDE,
        }
        if where:
            options["where"] = where

        result = get_p_andamento_model().findAndCountAll(options)
        total = int(result.get("count") or 0)
        rows = result.get("rows") or []

        return {
            "rows": [self._map_andamento_row_with_include(row) for row in rows],
            "pagination": IndexRepository._build_pagination_meta(page, per_page, total),
        }

    def _execute_sql(
        self,
        index_filters: PAndamentoIndexSchema,
        page: int,
        per_page: int,
        sort_field: str,
        sort_direction: str,
    ) -> dict[str, Any]:
        where_clauses, params = IndexRepository._build_sql_filters(index_filters)
        where_clauses_pa = [clause.replace("P_ANDAMENTO", "PA") for clause in where_clauses]
        where_sql_pa = IndexRepository._where_sql(where_clauses_pa)
        offset = (page - 1) * per_page

        count_sql = f"SELECT COUNT(*) AS TOTAL FROM P_ANDAMENTO PA{where_sql_pa}"
        count_row = self.fetch_one(count_sql, params) or {}
        total = int(count_row.get("TOTAL") or count_row.get("total") or 0)

        sql = f"""
        SELECT FIRST {per_page} SKIP {offset}
            {_SELECT_JOIN_COLUMNS.strip()}
        FROM P_ANDAMENTO PA
        LEFT JOIN P_OCORRENCIA_ANDAMENTO POA
            ON POA.OCORRENCIA_ANDAMENTO_ID = PA.OCORRENCIA_ANDAMENTO_ID
        {where_sql_pa}
        ORDER BY PA.{sort_field} {sort_direction.upper()}
        """
        rows = self.fetch_all(sql, params)

        return {
            "rows": [self._map_andamento_row_with_include(row) for row in rows],
            "pagination": IndexRepository._build_pagination_meta(page, per_page, total),
        }

    @staticmethod
    def _map_ocorrencia_andamento_embed(
        value: Optional[Mapping[str, Any]],
    ) -> Optional[dict[str, Any]]:
        if value is None:
            return None
        mapped = normalize_row_keys(value)
        if mapped is None:
            return None

        ocorrencia_id = mapped.get("ocorrencia_andamento_id")
        if isinstance(ocorrencia_id, Decimal):
            mapped["ocorrencia_andamento_id"] = int(ocorrencia_id)

        codigo = mapped.get("codigo")
        if codigo is not None:
            mapped["codigo"] = str(codigo).strip().upper() or None

        descricao = mapped.get("descricao")
        if descricao is not None:
            mapped["descricao"] = str(descricao).strip() or None

        if mapped.get("ocorrencia_andamento_id") is None and not mapped.get("codigo"):
            return None

        return mapped

    @classmethod
    def _map_andamento_row_with_include(
        cls, row: Optional[Mapping[str, Any]]
    ) -> dict[str, Any]:
        mapped = normalize_row_keys(row)
        if mapped is None:
            return {}

        nested = mapped.pop("ocorrencia_andamento", None)
        if nested is None:
            oca_codigo = mapped.pop("oca_codigo", None)
            oca_descricao = mapped.pop("oca_descricao", None)
            ocorrencia_id = mapped.get("ocorrencia_andamento_id")
            if ocorrencia_id is not None or oca_codigo or oca_descricao:
                nested = {
                    "ocorrencia_andamento_id": ocorrencia_id,
                    "codigo": oca_codigo,
                    "descricao": oca_descricao,
                }

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

        mapped["ocorrencia_andamento"] = cls._map_ocorrencia_andamento_embed(nested)
        return mapped
