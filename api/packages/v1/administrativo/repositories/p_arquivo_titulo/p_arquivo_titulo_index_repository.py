from __future__ import annotations

from datetime import timedelta
from typing import Any, Mapping, Optional

from orm_py import Op

from abstracts.repository import BaseRepository
from actions.data.query_params_parser import QueryParams, QueryParamsParser
from database.orm_firebird import firebird_orm_supports_string_where, normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_arquivo_titulo import get_p_arquivo_titulo_model
from packages.v1.administrativo.model.p_titulo import get_p_titulo_model
from packages.v1.administrativo.repositories.p_arquivo_titulo.p_arquivo_titulo_orm_helpers import (
    _ARQUIVO_TITULO_TITULOS_INCLUDE,
)
from packages.v1.administrativo.schemas.p_arquivo_titulo_schema import (
    PArquivoTituloIndexSchema,
    map_arquivo_titulo_row,
    map_titulos_numero_apontamento_list,
)

_PARQUIVO_TITULO_SORT_FIELD_MAP = {
    "arquivo_titulo_id": "ARQUIVO_TITULO_ID",
    "data_importacao": "DATA_IMPORTACAO",
    "nome_arquivo": "NOME_ARQUIVO",
    "portador_codigo": "PORTADOR_CODIGO",
    "quantidade": "QUANTIDADE",
    "soma_vlr_remessa": "SOMA_VLR_REMESSA",
}

_SELECT_COLUMNS = """
    ARQUIVO_TITULO_ID,
    DATA_IMPORTACAO,
    QUANTIDADE,
    DATA_MOVIMENTO,
    NUMERO_SEQUENCIAL,
    QTDE_REGISTROS,
    QTDE_TITULOS,
    QTDE_INDICACOES,
    QTDE_ORIGINAIS,
    SOMA_VLR_REMESSA,
    SOMA_QTDE_REMESSA,
    AGENCIA_CENTRALIZADORA,
    CODIGO_PRACA,
    SEQUENCIAL_HEADER,
    NOME_ARQUIVO,
    PORTADOR_NOME,
    COMPLEMENTO_HEADER,
    IDENTIFICACAO_REGISTRO,
    PORTADOR_CODIGO,
    ID_TRANSACAO_REMETENTE,
    ID_TRANSACAO_DESTINATARIO,
    ID_TRANSACAO_TIPO,
    VERSAO_LAYOUT,
    SEQUENCIAL_FOOTER,
    COMPLEMENTO_REGISTRO
"""

_SELECT_ATTRIBUTES = [column.strip() for column in _SELECT_COLUMNS.split(",")]


class IndexRepository(BaseRepository):
    def execute(
        self,
        arquivo_index_schema: PArquivoTituloIndexSchema,
        query_params: QueryParams,
    ) -> dict[str, Any]:
        page = query_params.page
        per_page = query_params.per_page
        sort_field, sort_direction = QueryParamsParser.resolve_sort(
            query_params,
            primary_key="arquivo_titulo_id",
            field_map=_PARQUIVO_TITULO_SORT_FIELD_MAP,
        )

        if use_orm_firebird() and (
            firebird_orm_supports_string_where()
            or not self._has_string_filters(arquivo_index_schema)
        ):
            return self._execute_orm(
                arquivo_index_schema, page, per_page, sort_field, sort_direction
            )
        return self._execute_sql(
            arquivo_index_schema, page, per_page, sort_field, sort_direction
        )

    def _execute_orm(
        self,
        arquivo_index_schema: PArquivoTituloIndexSchema,
        page: int,
        per_page: int,
        sort_field: str,
        sort_direction: str,
    ) -> dict[str, Any]:
        where = self._build_orm_where(arquivo_index_schema)
        offset = (page - 1) * per_page
        include_titulos = self._includes_titulos(arquivo_index_schema)

        options: dict[str, Any] = {
            "attributes": _SELECT_ATTRIBUTES,
            "order": [(sort_field, sort_direction.upper())],
            "limit": per_page,
            "offset": offset,
        }
        if where:
            options["where"] = where
        if include_titulos:
            options["include"] = _ARQUIVO_TITULO_TITULOS_INCLUDE

        result = get_p_arquivo_titulo_model().findAndCountAll(options)
        total = int(result.get("count") or 0)
        rows = result.get("rows") or []

        mapped_rows = [
            self._map_index_row(row, arquivo_index_schema) for row in rows
        ]
        if include_titulos:
            mapped_rows = self._enrich_titulos_numero_apontamento(
                mapped_rows, arquivo_index_schema, force=False
            )

        return {
            "rows": mapped_rows,
            "pagination": self._build_pagination_meta(page, per_page, total),
        }

    def _execute_sql(
        self,
        arquivo_index_schema: PArquivoTituloIndexSchema,
        page: int,
        per_page: int,
        sort_field: str,
        sort_direction: str,
    ) -> dict[str, Any]:
        where_clauses, params = self._build_sql_filters(arquivo_index_schema)
        where_sql = self._where_sql(where_clauses)
        offset = (page - 1) * per_page

        count_sql = f"SELECT COUNT(*) AS TOTAL FROM P_ARQUIVO_TITULO{where_sql}"
        count_row = self.fetch_one(count_sql, params) or {}
        total = int(count_row.get("TOTAL") or count_row.get("total") or 0)

        sql = f"""
        SELECT FIRST {per_page} SKIP {offset}
            {_SELECT_COLUMNS.strip()}
        FROM P_ARQUIVO_TITULO
        {where_sql}
        ORDER BY {sort_field} {sort_direction.upper()}
        """
        rows = self.fetch_all(sql, params)

        mapped_rows = [
            self._map_index_row(row, arquivo_index_schema) for row in rows
        ]
        if self._includes_titulos(arquivo_index_schema):
            mapped_rows = self._enrich_titulos_numero_apontamento(
                mapped_rows, arquivo_index_schema, force=True
            )

        return {
            "rows": mapped_rows,
            "pagination": self._build_pagination_meta(page, per_page, total),
        }

    @staticmethod
    def _includes_titulos(arquivo_index_schema: PArquivoTituloIndexSchema) -> bool:
        return "titulos" in arquivo_index_schema.includes

    def _map_index_row(
        self,
        row: Mapping[str, Any],
        arquivo_index_schema: PArquivoTituloIndexSchema,
    ) -> dict[str, Any]:
        row_dict = dict(row)
        titulos_raw = None
        if self._includes_titulos(arquivo_index_schema):
            titulos_raw = row_dict.pop("titulos", None) or row_dict.pop("TITULOS", None)

        arquivo = map_arquivo_titulo_row(row_dict) or {}
        if self._includes_titulos(arquivo_index_schema):
            if titulos_raw is not None:
                arquivo["titulos"] = map_titulos_numero_apontamento_list(titulos_raw)
            else:
                arquivo["titulos"] = []

        return arquivo

    def _enrich_titulos_numero_apontamento(
        self,
        rows: list[dict[str, Any]],
        arquivo_index_schema: PArquivoTituloIndexSchema,
        *,
        force: bool,
    ) -> list[dict[str, Any]]:
        if not self._includes_titulos(arquivo_index_schema):
            return rows

        if force:
            arquivo_ids = [
                int(row["arquivo_titulo_id"])
                for row in rows
                if row.get("arquivo_titulo_id") is not None
            ]
        else:
            arquivo_ids = [
                int(row["arquivo_titulo_id"])
                for row in rows
                if row.get("arquivo_titulo_id") is not None and not row.get("titulos")
            ]

        if not arquivo_ids:
            return rows

        titulos_by_arquivo = self._load_titulos_numero_apontamento_by_arquivo_ids(
            arquivo_ids
        )
        for row in rows:
            arquivo_id = row.get("arquivo_titulo_id")
            if arquivo_id is None:
                continue
            if force or not row.get("titulos"):
                row["titulos"] = titulos_by_arquivo.get(int(arquivo_id), [])

        return rows

    def _load_titulos_numero_apontamento_by_arquivo_ids(
        self, arquivo_titulo_ids: list[int]
    ) -> dict[int, list[dict[str, Any]]]:
        if not arquivo_titulo_ids:
            return {}

        titulo_rows = get_p_titulo_model().findAll(
            {
                "where": {"ARQUIVO_TITULO_ID": {Op.in_: arquivo_titulo_ids}},
                "attributes": ["ARQUIVO_TITULO_ID", "NUMERO_APONTAMENTO"],
                "order": [("ARQUIVO_TITULO_ID", "ASC"), ("TITULO_ID", "ASC")],
            }
        )

        grouped: dict[int, list[dict[str, Any]]] = {
            arquivo_id: [] for arquivo_id in arquivo_titulo_ids
        }
        for item in titulo_rows or []:
            row = normalize_row_keys(item)
            if row is None:
                continue
            arquivo_id = row.get("arquivo_titulo_id")
            if arquivo_id is None:
                continue
            arquivo_id = int(arquivo_id)
            if arquivo_id not in grouped:
                grouped[arquivo_id] = []
            grouped[arquivo_id].extend(map_titulos_numero_apontamento_list([row]))

        return grouped

    @staticmethod
    def _has_string_filters(arquivo_index_schema: PArquivoTituloIndexSchema) -> bool:
        return any(
            [
                arquivo_index_schema.nome_arquivo is not None,
                arquivo_index_schema.portador_codigo is not None,
                arquivo_index_schema.codigo_praca is not None,
            ]
        )

    @staticmethod
    def _build_orm_where(
        arquivo_index_schema: PArquivoTituloIndexSchema,
    ) -> dict[str, Any]:
        clauses: list[dict[str, Any]] = []

        if arquivo_index_schema.nome_arquivo is not None:
            clauses.append(
                {"NOME_ARQUIVO": {Op.like: f"%{arquivo_index_schema.nome_arquivo}%"}}
            )
        if arquivo_index_schema.portador_codigo is not None:
            clauses.append({"PORTADOR_CODIGO": arquivo_index_schema.portador_codigo})
        if arquivo_index_schema.codigo_praca is not None:
            clauses.append({"CODIGO_PRACA": arquivo_index_schema.codigo_praca})
        if arquivo_index_schema.data_inicio is not None:
            clauses.append(
                {"DATA_IMPORTACAO": {Op.gte: arquivo_index_schema.data_inicio}}
            )
        if arquivo_index_schema.data_fim is not None:
            clauses.append(
                {
                    "DATA_IMPORTACAO": {
                        Op.lt: arquivo_index_schema.data_fim + timedelta(days=1)
                    }
                }
            )

        if not clauses:
            return {}
        if len(clauses) == 1:
            return clauses[0]
        return {Op.and_: clauses}

    def _build_sql_filters(
        self, arquivo_index_schema: PArquivoTituloIndexSchema
    ) -> tuple[list[str], dict[str, Any]]:
        where: list[str] = []
        params: dict[str, Any] = {}

        if arquivo_index_schema.nome_arquivo is not None:
            where.append("UPPER(NOME_ARQUIVO) LIKE UPPER(:nome_arquivo)")
            params["nome_arquivo"] = f"%{arquivo_index_schema.nome_arquivo}%"
        if arquivo_index_schema.portador_codigo is not None:
            where.append("UPPER(TRIM(PORTADOR_CODIGO)) = :portador_codigo")
            params["portador_codigo"] = arquivo_index_schema.portador_codigo
        if arquivo_index_schema.codigo_praca is not None:
            where.append("CODIGO_PRACA = :codigo_praca")
            params["codigo_praca"] = arquivo_index_schema.codigo_praca
        if arquivo_index_schema.data_inicio is not None:
            where.append("CAST(DATA_IMPORTACAO AS DATE) >= :data_inicio")
            params["data_inicio"] = arquivo_index_schema.data_inicio
        if arquivo_index_schema.data_fim is not None:
            where.append("CAST(DATA_IMPORTACAO AS DATE) <= :data_fim")
            params["data_fim"] = arquivo_index_schema.data_fim

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
