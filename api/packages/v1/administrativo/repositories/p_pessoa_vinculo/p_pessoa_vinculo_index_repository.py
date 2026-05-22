from __future__ import annotations

from typing import Any

from orm_py import Op

from abstracts.repository import BaseRepository
from actions.data.query_params_parser import QueryParams, QueryParamsParser
from database.orm_firebird import firebird_orm_supports_string_where
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_pessoa_vinculo import get_p_pessoa_vinculo_model
from packages.v1.administrativo.schemas.p_pessoa_vinculo_schema import (
    PPessoaVinculoIndexSchema,
    map_pessoa_vinculo_row,
)

_PPESSOA_VINCULO_SORT_FIELD_MAP = {
    "pessoa_vinculo_id": "PESSOA_VINCULO_ID",
    "titulo_id": "TITULO_ID",
    "pessoa_id": "PESSOA_ID",
    "nome": "NOME",
    "cpfcnpj": "CPFCNPJ",
    "tipo_vinculo": "TIPO_VINCULO",
    "cidade": "CIDADE",
    "uf": "UF",
}

_SELECT_COLUMNS = """
    PESSOA_VINCULO_ID,
    NOME,
    CPFCNPJ,
    ENDERECO,
    BAIRRO,
    CIDADE,
    UF,
    CEP,
    TELEFONE,
    RG,
    TITULO_ID,
    TIPO_VINCULO,
    PESSOA_ID,
    BANCO,
    AGENCIA,
    CONTA,
    NOME_BANCO,
    NACIONALIDADE,
    ESTADO_CIVIL_ID,
    PROFISSAO_ID,
    CIDADE_AGENCIA,
    GERAR_SELO,
    DEVEDOR_DATA_ACEITE,
    DEVEDOR_AGENCIA,
    DEVEDOR_NUMERO_AR,
    DEVEDOR_RECEBIDO_POR,
    DEVEDOR_SITUACAO,
    DEVEDOR_TIPO_ACEITE,
    OCORRENCIA_ID,
    CHAVE_IMPORTACAO,
    DEVEDOR_MICROEMPRESA,
    OCORRENCIA_ANDAMENTO_ID,
    CONTROLE_DEVEDOR
"""


class IndexRepository(BaseRepository):
    def execute(
        self,
        vinculo_index_schema: PPessoaVinculoIndexSchema,
        query_params: QueryParams,
    ) -> dict[str, Any]:
        page = query_params.page
        per_page = query_params.per_page
        sort_field, sort_direction = QueryParamsParser.resolve_sort(
            query_params,
            primary_key="pessoa_vinculo_id",
            field_map=_PPESSOA_VINCULO_SORT_FIELD_MAP,
        )

        if use_orm_firebird() and (
            firebird_orm_supports_string_where()
            or not self._has_string_filters(vinculo_index_schema)
        ):
            return self._execute_orm(
                vinculo_index_schema, page, per_page, sort_field, sort_direction
            )
        return self._execute_sql(
            vinculo_index_schema, page, per_page, sort_field, sort_direction
        )

    def _execute_orm(
        self,
        vinculo_index_schema: PPessoaVinculoIndexSchema,
        page: int,
        per_page: int,
        sort_field: str,
        sort_direction: str,
    ) -> dict[str, Any]:
        where = self._build_orm_where(vinculo_index_schema)
        offset = (page - 1) * per_page

        options: dict[str, Any] = {
            "order": [(sort_field, sort_direction.upper())],
            "limit": per_page,
            "offset": offset,
        }
        if where:
            options["where"] = where

        result = get_p_pessoa_vinculo_model().findAndCountAll(options)
        total = int(result.get("count") or 0)
        rows = result.get("rows") or []

        return {
            "rows": [map_pessoa_vinculo_row(row) or {} for row in rows],
            "pagination": self._build_pagination_meta(page, per_page, total),
        }

    def _execute_sql(
        self,
        vinculo_index_schema: PPessoaVinculoIndexSchema,
        page: int,
        per_page: int,
        sort_field: str,
        sort_direction: str,
    ) -> dict[str, Any]:
        where_clauses, params = self._build_sql_filters(vinculo_index_schema)
        where_sql = self._where_sql(where_clauses)
        offset = (page - 1) * per_page

        count_sql = f"SELECT COUNT(*) AS TOTAL FROM P_PESSOA_VINCULO{where_sql}"
        count_row = self.fetch_one(count_sql, params) or {}
        total = int(count_row.get("TOTAL") or count_row.get("total") or 0)

        sql = f"""
        SELECT FIRST {per_page} SKIP {offset}
            {_SELECT_COLUMNS.strip()}
        FROM P_PESSOA_VINCULO
        {where_sql}
        ORDER BY {sort_field} {sort_direction.upper()}
        """
        rows = self.fetch_all(sql, params)

        return {
            "rows": [map_pessoa_vinculo_row(row) or {} for row in rows],
            "pagination": self._build_pagination_meta(page, per_page, total),
        }

    @staticmethod
    def _has_string_filters(vinculo_index_schema: PPessoaVinculoIndexSchema) -> bool:
        return any(
            [
                vinculo_index_schema.tipo_vinculo is not None,
                vinculo_index_schema.nome is not None,
                vinculo_index_schema.cpfcnpj is not None,
                vinculo_index_schema.busca is not None,
            ]
        )

    @staticmethod
    def _build_orm_where(vinculo_index_schema: PPessoaVinculoIndexSchema) -> dict[str, Any]:
        clauses: list[dict[str, Any]] = []

        if vinculo_index_schema.titulo_id is not None:
            clauses.append({"TITULO_ID": vinculo_index_schema.titulo_id})
        if vinculo_index_schema.pessoa_id is not None:
            clauses.append({"PESSOA_ID": vinculo_index_schema.pessoa_id})
        if vinculo_index_schema.tipo_vinculo is not None:
            clauses.append({"TIPO_VINCULO": vinculo_index_schema.tipo_vinculo})
        if vinculo_index_schema.nome is not None:
            clauses.append({"NOME": {Op.like: f"%{vinculo_index_schema.nome}%"}})
        if vinculo_index_schema.cpfcnpj is not None:
            clauses.append({"CPFCNPJ": {Op.like: f"%{vinculo_index_schema.cpfcnpj}%"}})
        if vinculo_index_schema.busca is not None:
            term = vinculo_index_schema.busca
            clauses.append(
                {
                    Op.or_: [
                        {"NOME": {Op.like: f"%{term}%"}},
                        {"CPFCNPJ": {Op.like: f"%{term}%"}},
                    ]
                }
            )

        if not clauses:
            return {}
        if len(clauses) == 1:
            return clauses[0]
        return {Op.and_: clauses}

    def _build_sql_filters(
        self, vinculo_index_schema: PPessoaVinculoIndexSchema
    ) -> tuple[list[str], dict[str, Any]]:
        where: list[str] = []
        params: dict[str, Any] = {}

        if vinculo_index_schema.titulo_id is not None:
            where.append("TITULO_ID = :titulo_id")
            params["titulo_id"] = vinculo_index_schema.titulo_id
        if vinculo_index_schema.pessoa_id is not None:
            where.append("PESSOA_ID = :pessoa_id")
            params["pessoa_id"] = vinculo_index_schema.pessoa_id
        if vinculo_index_schema.tipo_vinculo is not None:
            where.append("UPPER(TRIM(TIPO_VINCULO)) = UPPER(:tipo_vinculo)")
            params["tipo_vinculo"] = vinculo_index_schema.tipo_vinculo
        if vinculo_index_schema.nome is not None:
            where.append("UPPER(NOME) LIKE UPPER(:nome)")
            params["nome"] = f"%{vinculo_index_schema.nome}%"
        if vinculo_index_schema.cpfcnpj is not None:
            where.append("CPFCNPJ LIKE :cpfcnpj")
            params["cpfcnpj"] = f"%{vinculo_index_schema.cpfcnpj}%"
        if vinculo_index_schema.busca is not None:
            where.append(
                "(UPPER(NOME) LIKE UPPER(:busca) OR CPFCNPJ LIKE :busca)"
            )
            params["busca"] = f"%{vinculo_index_schema.busca}%"

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
