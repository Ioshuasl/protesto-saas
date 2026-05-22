from __future__ import annotations

from typing import Any

from orm_py import Op

from abstracts.repository import BaseRepository
from actions.data.query_params_parser import QueryParams, QueryParamsParser
from database.orm_firebird import firebird_orm_supports_string_where, normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_pessoa import get_p_pessoa_model
from packages.v1.administrativo.repositories.p_pessoa.p_pessoa_count_titulos_by_pessoa_ids_repository import (
    CountTitulosByPessoaIdsRepository,
)
from packages.v1.administrativo.schemas.p_pessoa_schema import (
    CNPJ_DIGITOS,
    CPF_DIGITOS,
    PPessoaIndexSchema,
    TIPO_PESSOA_FISICA,
    TIPO_PESSOA_JURIDICA,
    infer_tipo_pessoa_from_cpfcnpj,
    map_pessoa_row,
)

_PPESSOA_SORT_FIELD_MAP = {
    "pessoa_id": "PESSOA_ID",
    "nome": "NOME",
    "cpfcnpj": "CPFCNPJ",
    "cidade": "CIDADE",
    "uf": "UF",
    "telefone": "TELEFONE",
}

# CPFCNPJ e TELEFONE são VARCHAR(15) — LIKE com % nos dois lados estoura o bind.
_VARCHAR_15_LIKE_PREFIX_MAX = 14

# Limite por ramo da busca unificada (nome → cpfcnpj → telefone).
_BUSCA_BRANCH_LIMIT = 1000

_SELECT_COLUMNS = """
    PESSOA_ID,
    NOME,
    CPFCNPJ,
    ENDERECO,
    BAIRRO,
    CIDADE,
    UF,
    CEP,
    TELEFONE,
    RG,
    OBSERVACOES,
    BANCO,
    AGENCIA,
    CONTA,
    NOME_BANCO,
    NACIONALIDADE,
    ESTADO_CIVIL_ID,
    PROFISSAO_ID,
    CIDADE_AGENCIA,
    DATA_NASCIMENTO,
    EMAIL,
    CIDADE_ID,
    DATA_VALIDADE,
    MICRO_EMPRESA,
    CHAVE_PESSOA_IMP,
    COD_CRA,
    NOME_FANTASIA
"""


def _digits_only(value: str) -> str:
    return "".join(ch for ch in value if ch.isdigit())


def _varchar15_like_prefix(value: str) -> str:
    compact = _digits_only(value) or value.strip()
    return f"{compact[:_VARCHAR_15_LIKE_PREFIX_MAX]}%"


_CPFCNPJ_STRIP_CHARS = ".-/ \\(),"


def _cpfcnpj_digits_length_sql() -> str:
    expr = "TRIM(COALESCE(CPFCNPJ, ''))"
    for char in _CPFCNPJ_STRIP_CHARS:
        expr = f"REPLACE({expr}, '{char}', '')"
    return f"CHAR_LENGTH({expr})"


def _tipo_pessoa_digit_length(tipo_pessoa: str) -> int:
    if tipo_pessoa == TIPO_PESSOA_FISICA:
        return CPF_DIGITOS
    if tipo_pessoa == TIPO_PESSOA_JURIDICA:
        return CNPJ_DIGITOS
    raise ValueError(f"Tipo de pessoa inválido: {tipo_pessoa}")


class IndexRepository(BaseRepository):
    def execute(
        self,
        pessoa_index_schema: PPessoaIndexSchema,
        query_params: QueryParams,
    ) -> dict[str, Any]:
        page = query_params.page
        per_page = query_params.per_page
        sort_field, sort_direction = QueryParamsParser.resolve_sort(
            query_params,
            primary_key="pessoa_id",
            field_map=_PPESSOA_SORT_FIELD_MAP,
        )

        if pessoa_index_schema.busca:
            return self._execute_busca_unificada(
                pessoa_index_schema,
                page,
                per_page,
                sort_field,
                sort_direction,
            )

        # Filtro por quantidade de dígitos do documento só existe no SQL.
        if pessoa_index_schema.tipo_pessoa is not None:
            return self._execute_sql(
                pessoa_index_schema, page, per_page, sort_field, sort_direction
            )

        if use_orm_firebird() and (
            firebird_orm_supports_string_where()
            or not self._has_location_filters(pessoa_index_schema)
        ):
            return self._execute_orm(
                pessoa_index_schema, page, per_page, sort_field, sort_direction
            )
        return self._execute_sql(
            pessoa_index_schema, page, per_page, sort_field, sort_direction
        )

    def _execute_busca_unificada(
        self,
        pessoa_index_schema: PPessoaIndexSchema,
        page: int,
        per_page: int,
        sort_field: str,
        sort_direction: str,
    ) -> dict[str, Any]:
        busca = pessoa_index_schema.busca or ""
        seen_ids: set[int] = set()
        merged: list[dict[str, Any]] = []

        for fetch_fn in (
            self._fetch_rows_by_nome,
            self._fetch_rows_by_cpfcnpj,
            self._fetch_rows_by_telefone,
        ):
            rows = fetch_fn(pessoa_index_schema, busca, seen_ids)
            for row in rows:
                pessoa_id = row.get("pessoa_id")
                if pessoa_id is None or pessoa_id in seen_ids:
                    continue
                seen_ids.add(int(pessoa_id))
                merged.append(row)

        merged = self._filter_rows_by_tipo_pessoa(merged, pessoa_index_schema)
        merged = self._sort_rows(merged, sort_field, sort_direction)
        total = len(merged)
        offset = (page - 1) * per_page
        page_rows = merged[offset : offset + per_page]

        return {
            "rows": self._enrich_rows_with_total_titulos(page_rows),
            "pagination": self._build_pagination_meta(page, per_page, total),
        }

    def _fetch_rows_by_nome(
        self,
        schema: PPessoaIndexSchema,
        busca: str,
        exclude_ids: set[int],
    ) -> list[dict[str, Any]]:
        where, params = self._build_location_sql_filters(schema)
        where.append("UPPER(NOME) LIKE UPPER(:busca_nome)")
        params["busca_nome"] = f"%{busca}%"
        self._append_exclude_ids(where, exclude_ids, params, "nome")
        return self._fetch_rows_limited(where, params)

    def _fetch_rows_by_cpfcnpj(
        self,
        schema: PPessoaIndexSchema,
        busca: str,
        exclude_ids: set[int],
    ) -> list[dict[str, Any]]:
        where, params = self._build_location_sql_filters(schema)
        where.append("UPPER(CPFCNPJ) LIKE UPPER(:busca_cpfcnpj)")
        params["busca_cpfcnpj"] = _varchar15_like_prefix(busca)
        self._append_exclude_ids(where, exclude_ids, params, "cpf")
        return self._fetch_rows_limited(where, params)

    def _fetch_rows_by_telefone(
        self,
        schema: PPessoaIndexSchema,
        busca: str,
        exclude_ids: set[int],
    ) -> list[dict[str, Any]]:
        where, params = self._build_location_sql_filters(schema)
        where.append("UPPER(TELEFONE) LIKE UPPER(:busca_telefone)")
        params["busca_telefone"] = _varchar15_like_prefix(busca)
        self._append_exclude_ids(where, exclude_ids, params, "tel")
        return self._fetch_rows_limited(where, params)

    def _fetch_rows_limited(
        self, where: list[str], params: dict[str, Any]
    ) -> list[dict[str, Any]]:
        where_sql = self._where_sql(where)
        sql = f"""
        SELECT FIRST {_BUSCA_BRANCH_LIMIT}
            {_SELECT_COLUMNS.strip()}
        FROM P_PESSOA
        {where_sql}
        ORDER BY PESSOA_ID DESC
        """
        rows = self.fetch_all(sql, params)
        return [map_pessoa_row(normalize_row_keys(row)) or {} for row in rows]

    @staticmethod
    def _append_exclude_ids(
        where: list[str],
        exclude_ids: set[int],
        params: dict[str, Any],
        prefix: str,
    ) -> None:
        if not exclude_ids:
            return
        placeholders: list[str] = []
        for index, pessoa_id in enumerate(sorted(exclude_ids)):
            key = f"ex_{prefix}_{index}"
            params[key] = pessoa_id
            placeholders.append(f":{key}")
        where.append(f"PESSOA_ID NOT IN ({', '.join(placeholders)})")

    def _build_location_sql_filters(
        self, schema: PPessoaIndexSchema
    ) -> tuple[list[str], dict[str, Any]]:
        where: list[str] = []
        params: dict[str, Any] = {}
        if schema.cidade is not None:
            where.append("UPPER(TRIM(CIDADE)) = UPPER(TRIM(:cidade))")
            params["cidade"] = schema.cidade
        if schema.uf is not None:
            where.append("UPPER(TRIM(UF)) = UPPER(TRIM(:uf))")
            params["uf"] = schema.uf
        self._append_tipo_pessoa_sql_filter(where, schema)
        return where, params

    @staticmethod
    def _append_tipo_pessoa_sql_filter(
        where: list[str], schema: PPessoaIndexSchema
    ) -> None:
        if schema.tipo_pessoa is None:
            return
        expected = _tipo_pessoa_digit_length(schema.tipo_pessoa)
        where.append(f"{_cpfcnpj_digits_length_sql()} = {expected}")

    @staticmethod
    def _filter_rows_by_tipo_pessoa(
        rows: list[dict[str, Any]], schema: PPessoaIndexSchema
    ) -> list[dict[str, Any]]:
        if schema.tipo_pessoa is None:
            return rows
        return [
            row
            for row in rows
            if infer_tipo_pessoa_from_cpfcnpj(row.get("cpfcnpj"))
            == schema.tipo_pessoa
        ]

    @staticmethod
    def _sort_rows(
        rows: list[dict[str, Any]], sort_field: str, sort_direction: str
    ) -> list[dict[str, Any]]:
        reverse = sort_direction.lower() == "desc"

        field_key = sort_field.lower()

        def sort_key(row: dict[str, Any]) -> Any:
            value = row.get(field_key)
            if value is None:
                return ""
            return value

        return sorted(rows, key=sort_key, reverse=reverse)

    def _execute_orm(
        self,
        pessoa_index_schema: PPessoaIndexSchema,
        page: int,
        per_page: int,
        sort_field: str,
        sort_direction: str,
    ) -> dict[str, Any]:
        where = self._build_orm_where(pessoa_index_schema)
        offset = (page - 1) * per_page

        options: dict[str, Any] = {
            "order": [(sort_field, sort_direction.upper())],
            "limit": per_page,
            "offset": offset,
        }
        if where:
            options["where"] = where

        result = get_p_pessoa_model().findAndCountAll(options)
        total = int(result.get("count") or 0)
        rows = result.get("rows") or []

        mapped_rows = [map_pessoa_row(row) or {} for row in rows]
        return {
            "rows": self._enrich_rows_with_total_titulos(mapped_rows),
            "pagination": self._build_pagination_meta(page, per_page, total),
        }

    def _execute_sql(
        self,
        pessoa_index_schema: PPessoaIndexSchema,
        page: int,
        per_page: int,
        sort_field: str,
        sort_direction: str,
    ) -> dict[str, Any]:
        where_clauses, params = self._build_sql_filters(pessoa_index_schema)
        where_sql = self._where_sql(where_clauses)
        offset = (page - 1) * per_page

        count_sql = f"SELECT COUNT(*) AS TOTAL FROM P_PESSOA{where_sql}"
        count_row = self.fetch_one(count_sql, params) or {}
        total = int(count_row.get("TOTAL") or count_row.get("total") or 0)

        sql = f"""
        SELECT FIRST {per_page} SKIP {offset}
            {_SELECT_COLUMNS.strip()}
        FROM P_PESSOA
        {where_sql}
        ORDER BY {sort_field} {sort_direction.upper()}
        """
        rows = self.fetch_all(sql, params)
        mapped_rows = [
            map_pessoa_row(normalize_row_keys(row)) or {} for row in rows
        ]

        return {
            "rows": self._enrich_rows_with_total_titulos(mapped_rows),
            "pagination": self._build_pagination_meta(page, per_page, total),
        }

    def _enrich_rows_with_total_titulos(
        self, rows: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        pessoa_ids = [
            int(row["pessoa_id"])
            for row in rows
            if row.get("pessoa_id") is not None
        ]
        counts = CountTitulosByPessoaIdsRepository().execute(pessoa_ids)
        for row in rows:
            pessoa_id = row.get("pessoa_id")
            row["total_titulos"] = (
                counts.get(int(pessoa_id), 0) if pessoa_id is not None else 0
            )
        return rows

    @staticmethod
    def _has_location_filters(pessoa_index_schema: PPessoaIndexSchema) -> bool:
        return (
            pessoa_index_schema.cidade is not None
            or pessoa_index_schema.uf is not None
            or pessoa_index_schema.tipo_pessoa is not None
        )

    @staticmethod
    def _build_orm_where(pessoa_index_schema: PPessoaIndexSchema) -> dict[str, Any]:
        clauses: list[dict[str, Any]] = []

        if pessoa_index_schema.cidade is not None:
            clauses.append({"CIDADE": pessoa_index_schema.cidade})
        if pessoa_index_schema.uf is not None:
            clauses.append({"UF": pessoa_index_schema.uf})

        if not clauses:
            return {}
        if len(clauses) == 1:
            return clauses[0]
        return {Op.and_: clauses}

    def _build_sql_filters(
        self, pessoa_index_schema: PPessoaIndexSchema
    ) -> tuple[list[str], dict[str, Any]]:
        return self._build_location_sql_filters(pessoa_index_schema)

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
