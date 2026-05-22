from __future__ import annotations

from typing import Any

from abstracts.repository import BaseRepository
from actions.data.query_params_parser import QueryParams, QueryParamsParser
from packages.v1.administrativo.schemas.p_titulo_schema import (
    PTituloIndexSchema,
    map_titulo_index_row,
)

_PTITULO_INDEX_SORT_FIELD_MAP = {
    "titulo_id": "TITULO_ID",
    "numero_apontamento": "NUMERO_APONTAMENTO",
    "valor_titulo": "VALOR_TITULO",
    "ocorrencia_id": "OCORRENCIA_ID",
    "numero_titulo": "NUMERO_TITULO",
    "especie_id": "ESPECIE_ID",
    "banco_id": "BANCO_ID",
}

_TITULO_INDEX_FROM = """
FROM P_TITULO t
LEFT JOIN P_ESPECIE e ON e.ESPECIE_ID = t.ESPECIE_ID
LEFT JOIN P_OCORRENCIAS o ON o.OCORRENCIAS_ID = t.OCORRENCIA_ID
LEFT JOIN P_BANCO b ON b.BANCO_ID = t.BANCO_ID
"""

_TITULO_INDEX_SELECT = """
    t.TITULO_ID,
    t.NUMERO_TITULO,
    t.NOSSO_NUMERO,
    t.NUMERO_APONTAMENTO,
    t.ESPECIE_ID,
    e.ESPECIE AS ESPECIE_SIGLA,
    e.DESCRICAO AS ESPECIE_DESCRICAO,
    t.VALOR_TITULO,
    t.OCORRENCIA_ID,
    o.DESCRICAO AS OCORRENCIA_DESCRICAO,
    t.BANCO_ID,
    b.DESCRICAO AS BANCO_DESCRICAO,
    (
        SELECT COUNT(*)
        FROM P_PESSOA_VINCULO pv
        WHERE pv.TITULO_ID = t.TITULO_ID
    ) AS QTD_PESSOAS_VINCULADAS,
    (
        SELECT FIRST 1 pv.NOME
        FROM P_PESSOA_VINCULO pv
        WHERE pv.TITULO_ID = t.TITULO_ID
          AND UPPER(TRIM(pv.TIPO_VINCULO)) = 'APRESENTANTE'
        ORDER BY pv.PESSOA_VINCULO_ID
    ) AS APRESENTANTE_NOME,
    (
        SELECT FIRST 1 pv.CPFCNPJ
        FROM P_PESSOA_VINCULO pv
        WHERE pv.TITULO_ID = t.TITULO_ID
          AND UPPER(TRIM(pv.TIPO_VINCULO)) = 'APRESENTANTE'
        ORDER BY pv.PESSOA_VINCULO_ID
    ) AS APRESENTANTE_CPFCNPJ
"""


class IndexRepository(BaseRepository):
    def execute(
        self,
        titulo_index_schema: PTituloIndexSchema,
        query_params: QueryParams,
    ) -> dict[str, Any]:
        page = query_params.page
        per_page = query_params.per_page
        sort_field, sort_direction = QueryParamsParser.resolve_sort(
            query_params,
            primary_key="titulo_id",
            field_map=_PTITULO_INDEX_SORT_FIELD_MAP,
        )

        where_clauses, params = self._build_sql_filters(titulo_index_schema)
        where_sql = self._where_sql(where_clauses)
        offset = (page - 1) * per_page
        order_column = self._order_column(sort_field)

        count_sql = f"""
        SELECT COUNT(*) AS TOTAL
        {_TITULO_INDEX_FROM}
        {where_sql}
        """
        count_row = self.fetch_one(count_sql, params) or {}
        total = int(count_row.get("TOTAL") or count_row.get("total") or 0)

        if total == 0:
            return {
                "rows": [],
                "pagination": self._build_pagination_meta(page, per_page, 0),
            }

        sql = f"""
        SELECT FIRST {per_page} SKIP {offset}
            {_TITULO_INDEX_SELECT.strip()}
        {_TITULO_INDEX_FROM}
        {where_sql}
        ORDER BY {order_column} {sort_direction.upper()}
        """
        rows = self.fetch_all(sql, params)

        return {
            "rows": [map_titulo_index_row(row) or {} for row in rows],
            "pagination": self._build_pagination_meta(page, per_page, total),
        }

    def _build_sql_filters(
        self, titulo_index_schema: PTituloIndexSchema
    ) -> tuple[list[str], dict[str, Any]]:
        where: list[str] = []
        params: dict[str, Any] = {}

        if titulo_index_schema.numero_apontamento is not None:
            where.append("t.NUMERO_APONTAMENTO = :numero_apontamento")
            params["numero_apontamento"] = titulo_index_schema.numero_apontamento
        if titulo_index_schema.ocorrencia_id is not None:
            where.append("t.OCORRENCIA_ID = :ocorrencia_id")
            params["ocorrencia_id"] = titulo_index_schema.ocorrencia_id
        if titulo_index_schema.ocorrencia_andamento_id is not None:
            where.append("t.OCORRENCIA_ANDAMENTO_ID = :ocorrencia_andamento_id")
            params["ocorrencia_andamento_id"] = titulo_index_schema.ocorrencia_andamento_id
        if titulo_index_schema.banco_id is not None:
            where.append("t.BANCO_ID = :banco_id")
            params["banco_id"] = titulo_index_schema.banco_id
        if titulo_index_schema.especie_id is not None:
            where.append("t.ESPECIE_ID = :especie_id")
            params["especie_id"] = titulo_index_schema.especie_id

        if titulo_index_schema.nosso_numero is not None:
            where.append("UPPER(t.NOSSO_NUMERO) LIKE UPPER(:nosso_numero)")
            params["nosso_numero"] = f"%{titulo_index_schema.nosso_numero}%"
        if titulo_index_schema.numero_titulo is not None:
            where.append("UPPER(t.NUMERO_TITULO) LIKE UPPER(:numero_titulo)")
            params["numero_titulo"] = f"%{titulo_index_schema.numero_titulo}%"
        if titulo_index_schema.numero_titulo_banco is not None:
            where.append("UPPER(t.NUMERO_TITULO_BANCO) LIKE UPPER(:numero_titulo_banco)")
            params["numero_titulo_banco"] = f"%{titulo_index_schema.numero_titulo_banco}%"

        if titulo_index_schema.busca_pessoa is not None:
            where.append(
                """
                EXISTS (
                    SELECT 1
                    FROM P_PESSOA_VINCULO pv
                    LEFT JOIN P_PESSOA p ON p.PESSOA_ID = pv.PESSOA_ID
                    WHERE pv.TITULO_ID = t.TITULO_ID
                      AND (
                        UPPER(pv.NOME) LIKE UPPER(:busca_pessoa)
                        OR UPPER(pv.CPFCNPJ) LIKE UPPER(:busca_pessoa)
                        OR UPPER(p.NOME) LIKE UPPER(:busca_pessoa)
                        OR UPPER(p.CPFCNPJ) LIKE UPPER(:busca_pessoa)
                      )
                )
                """
            )
            params["busca_pessoa"] = f"%{titulo_index_schema.busca_pessoa}%"

        return where, params

    @staticmethod
    def _order_column(sort_field: str) -> str:
        column = _PTITULO_INDEX_SORT_FIELD_MAP.get(sort_field, "TITULO_ID")
        return f"t.{column}"

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
