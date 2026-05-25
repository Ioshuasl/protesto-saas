from __future__ import annotations

from decimal import Decimal, InvalidOperation
from typing import Any, Mapping

from orm_py import Op

from abstracts.repository import BaseRepository
from actions.data.query_params_parser import QueryParams, QueryParamsParser
from packages.v1.administrativo.model.p_titulo import get_p_titulo_model
from packages.v1.administrativo.schemas.p_titulo_schema import (
    PTituloIndexSchema,
    map_titulo_index_row,
)

_PTITULO_INDEX_SORT_FIELD_MAP = {
    "titulo_id": "TITULO_ID",
    "numero_apontamento": "NUMERO_APONTAMENTO",
    "numero_titulo": "NUMERO_TITULO",
    "numero_titulo_banco": "NUMERO_TITULO_BANCO",
    "nosso_numero": "NOSSO_NUMERO",
    "valor_titulo": "VALOR_TITULO",
    "ocorrencia_id": "OCORRENCIA_ID",
    "ocorrencia_andamento_id": "OCORRENCIA_ANDAMENTO_ID",
    "especie_id": "ESPECIE_ID",
    "banco_id": "BANCO_ID",
}

_TITULO_INDEX_INCLUDES: list[dict[str, Any]] = [
    {
        "association": "especie",
        "required": False,
        "attributes": ["ESPECIE_ID", "ESPECIE", "DESCRICAO"],
    },
    {
        "association": "ocorrencia",
        "required": False,
        "attributes": ["OCORRENCIAS_ID", "DESCRICAO"],
    },
    {
        "association": "banco",
        "required": False,
        "attributes": ["BANCO_ID", "CODIGO_BANCO", "DESCRICAO"],
    },
    {
        "association": "pessoa_vinculos",
        "required": False,
        "separate": True,
        "attributes": [
            "PESSOA_VINCULO_ID",
            "TITULO_ID",
            "TIPO_VINCULO",
            "NOME",
            "CPFCNPJ",
            "PESSOA_ID",
            "DEVEDOR_MICROEMPRESA",
        ],
        "order": [("PESSOA_VINCULO_ID", "ASC")],
        "include": [
            {
                "association": "pessoa",
                "required": False,
                "attributes": ["PESSOA_ID", "NOME", "CPFCNPJ", "MICRO_EMPRESA"],
            }
        ],
    },
]


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

        if titulo_index_schema.busca:
            return self._execute_busca_unificada(
                titulo_index_schema,
                titulo_index_schema.busca,
                page,
                per_page,
                sort_field,
                sort_direction,
            )

        offset = (page - 1) * per_page
        where = self._build_orm_where(titulo_index_schema)

        options: dict[str, Any] = {
            "include": _TITULO_INDEX_INCLUDES,
            "limit": per_page,
            "offset": offset,
            "order": [(sort_field, sort_direction.upper())],
        }
        if where:
            options["where"] = where

        result = get_p_titulo_model().findAndCountAll(options)
        total = int(result.get("count") or 0)
        rows = result.get("rows") or []

        return {
            "rows": [self._map_orm_index_row(row) for row in rows if row is not None],
            "pagination": self._build_pagination_meta(page, per_page, total),
        }

    def _execute_busca_unificada(
        self,
        titulo_index_schema: PTituloIndexSchema,
        busca: str,
        page: int,
        per_page: int,
        sort_field: str,
        sort_direction: str,
    ) -> dict[str, Any]:
        seen_ids: set[int] = set()
        ordered_ids: list[int] = []

        for where in self._build_busca_branch_wheres(titulo_index_schema, busca):
            rows = get_p_titulo_model().findAll(
                {
                    "where": where,
                    "attributes": ["TITULO_ID"],
                    "order": [(sort_field, sort_direction.upper())],
                }
            )
            for row in rows or []:
                titulo_id = _int_or_none(_mapping_or_empty(row).get("TITULO_ID"))
                if titulo_id is None:
                    continue
                if titulo_id in seen_ids:
                    continue
                seen_ids.add(titulo_id)
                ordered_ids.append(titulo_id)

        total = len(ordered_ids)
        offset = (page - 1) * per_page
        page_ids = ordered_ids[offset : offset + per_page]
        if not page_ids:
            return {
                "rows": [],
                "pagination": self._build_pagination_meta(page, per_page, total),
            }

        rows = get_p_titulo_model().findAll(
            {
                "where": {"TITULO_ID": {Op.in_: page_ids}},
                "include": _TITULO_INDEX_INCLUDES,
                "order": [(sort_field, sort_direction.upper())],
            }
        )
        rows_by_id: dict[int, dict[str, Any]] = {}
        for row in rows or []:
            mapped = self._map_orm_index_row(row)
            titulo_id = _int_or_none(mapped.get("titulo_id"))
            if titulo_id is not None:
                rows_by_id[titulo_id] = mapped

        return {
            "rows": [rows_by_id[titulo_id] for titulo_id in page_ids if titulo_id in rows_by_id],
            "pagination": self._build_pagination_meta(page, per_page, total),
        }

    @classmethod
    def _build_busca_branch_wheres(
        cls,
        titulo_index_schema: PTituloIndexSchema,
        busca: str,
    ) -> list[dict[Any, Any]]:
        base_conditions = cls._build_base_orm_conditions(titulo_index_schema)
        text = busca.strip()
        nome_pattern = _safe_like_pattern(text, 150)
        cpfcnpj_pattern = _safe_like_pattern(text, 15)
        titulo_pattern = _safe_like_pattern(text, 30)
        numeric_value = _numero_apontamento_or_none(text)

        search_conditions: list[dict[Any, Any]] = []
        if nome_pattern:
            search_conditions.append(
                {
                    "pessoa_vinculos": {
                        Op.or_: [
                            {"NOME": {Op.like: nome_pattern}},
                            {"pessoa.NOME": {Op.like: nome_pattern}},
                        ]
                    }
                }
            )
        if cpfcnpj_pattern:
            search_conditions.append(
                {
                    "pessoa_vinculos": {
                        Op.or_: [
                            {"CPFCNPJ": {Op.like: cpfcnpj_pattern}},
                            {"pessoa.CPFCNPJ": {Op.like: cpfcnpj_pattern}},
                        ]
                    }
                }
            )
        if numeric_value is not None:
            search_conditions.append({"NUMERO_APONTAMENTO": numeric_value})
        if titulo_pattern:
            search_conditions.extend(
                [
                    {"NOSSO_NUMERO": {Op.like: titulo_pattern}},
                    {"NUMERO_TITULO": {Op.like: titulo_pattern}},
                    {"NUMERO_TITULO_BANCO": {Op.like: titulo_pattern}},
                ]
            )

        return [
            cls._combine_orm_conditions([*base_conditions, search_condition])
            for search_condition in search_conditions
        ]

    @staticmethod
    def _build_orm_where(titulo_index_schema: PTituloIndexSchema) -> dict[Any, Any]:
        conditions = IndexRepository._build_base_orm_conditions(titulo_index_schema)

        if titulo_index_schema.numero_apontamento is not None:
            conditions.append(
                {"NUMERO_APONTAMENTO": titulo_index_schema.numero_apontamento}
            )
        if titulo_index_schema.nosso_numero is not None:
            nosso_numero_pattern = _safe_like_pattern(
                titulo_index_schema.nosso_numero, 30
            )
            if nosso_numero_pattern:
                conditions.append({"NOSSO_NUMERO": {Op.like: nosso_numero_pattern}})
        if titulo_index_schema.numero_titulo is not None:
            numero_titulo_pattern = _safe_like_pattern(
                titulo_index_schema.numero_titulo, 30
            )
            if numero_titulo_pattern:
                conditions.append({"NUMERO_TITULO": {Op.like: numero_titulo_pattern}})
        if titulo_index_schema.numero_titulo_banco is not None:
            numero_titulo_banco_pattern = _safe_like_pattern(
                titulo_index_schema.numero_titulo_banco, 30
            )
            if numero_titulo_banco_pattern:
                conditions.append(
                    {"NUMERO_TITULO_BANCO": {Op.like: numero_titulo_banco_pattern}}
                )
        if titulo_index_schema.busca_pessoa is not None:
            nome_pattern = _safe_like_pattern(titulo_index_schema.busca_pessoa, 150)
            cpfcnpj_pattern = _safe_like_pattern(titulo_index_schema.busca_pessoa, 15)
            pessoa_filters: list[dict[Any, Any]] = []
            if nome_pattern:
                pessoa_filters.extend(
                    [
                        {"NOME": {Op.like: nome_pattern}},
                        {"pessoa.NOME": {Op.like: nome_pattern}},
                    ]
                )
            if cpfcnpj_pattern:
                pessoa_filters.extend(
                    [
                        {"CPFCNPJ": {Op.like: cpfcnpj_pattern}},
                        {"pessoa.CPFCNPJ": {Op.like: cpfcnpj_pattern}},
                    ]
                )
            if pessoa_filters:
                conditions.append({"pessoa_vinculos": {Op.or_: pessoa_filters}})

        return IndexRepository._combine_orm_conditions(conditions)

    @staticmethod
    def _build_base_orm_conditions(
        titulo_index_schema: PTituloIndexSchema,
    ) -> list[dict[Any, Any]]:
        conditions: list[dict[Any, Any]] = []
        if titulo_index_schema.ocorrencia_id is not None:
            conditions.append({"OCORRENCIA_ID": titulo_index_schema.ocorrencia_id})
        if titulo_index_schema.ocorrencia_andamento_id is not None:
            conditions.append(
                {"OCORRENCIA_ANDAMENTO_ID": titulo_index_schema.ocorrencia_andamento_id}
            )
        if titulo_index_schema.banco_id is not None:
            conditions.append({"BANCO_ID": titulo_index_schema.banco_id})
        if titulo_index_schema.especie_id is not None:
            conditions.append({"ESPECIE_ID": titulo_index_schema.especie_id})
        return conditions

    @staticmethod
    def _combine_orm_conditions(conditions: list[dict[Any, Any]]) -> dict[Any, Any]:
        if not conditions:
            return {}
        if len(conditions) == 1:
            return conditions[0]
        return {Op.and_: conditions}

    @staticmethod
    def _map_orm_index_row(row: Mapping[str, Any]) -> dict[str, Any]:
        especie = _mapping_or_empty(row.get("especie"))
        ocorrencia = _mapping_or_empty(row.get("ocorrencia"))
        banco = _mapping_or_empty(row.get("banco"))
        pessoa_vinculos = row.get("pessoa_vinculos")
        vinculos = pessoa_vinculos if isinstance(pessoa_vinculos, list) else []
        apresentante = _first_apresentante(vinculos)

        mapped_row = {
            "TITULO_ID": _decimal_or_original(row.get("TITULO_ID")),
            "DATA_INTIMACAO": row.get("DATA_INTIMACAO"),
            "DATA_PROTESTO": row.get("DATA_PROTESTO"),
            "DATA_ACEITE": row.get("DATA_ACEITE"),
            "DATA_APONTAMENTO": row.get("DATA_APONTAMENTO"),
            "DATA_CANCELAMENTO": row.get("DATA_CANCELAMENTO"),
            "DATA_EMISSAO_TITULO": row.get("DATA_EMISSAO_TITULO"),
            "DATA_CADASTRO": row.get("DATA_CADASTRO"),
            "DATA_SUSTADO": row.get("DATA_SUSTADO"),
            "DATA_PAGO": row.get("DATA_PAGO"),
            "LIVRO_ID_PROTESTO": _decimal_or_original(row.get("LIVRO_ID_PROTESTO")),
            "FOLHA_PROTESTO": _decimal_or_original(row.get("FOLHA_PROTESTO")),
            "NUMERO_TITULO": row.get("NUMERO_TITULO"),
            "NOSSO_NUMERO": row.get("NOSSO_NUMERO"),
            "NUMERO_APONTAMENTO": _decimal_or_original(row.get("NUMERO_APONTAMENTO")),
            "ESPECIE_ID": _decimal_or_original(row.get("ESPECIE_ID")),
            "ESPECIE_SIGLA": especie.get("ESPECIE"),
            "ESPECIE_DESCRICAO": especie.get("DESCRICAO"),
            "VALOR_TITULO": _decimal_or_original(row.get("VALOR_TITULO")),
            "OCORRENCIA_ID": _decimal_or_original(row.get("OCORRENCIA_ID")),
            "OCORRENCIA_DESCRICAO": ocorrencia.get("DESCRICAO"),
            "BANCO_ID": _decimal_or_original(row.get("BANCO_ID")),
            "BANCO_DESCRICAO": banco.get("DESCRICAO"),
            "QTD_PESSOAS_VINCULADAS": len(vinculos),
            "APRESENTANTE_NOME": apresentante.get("NOME"),
            "APRESENTANTE_CPFCNPJ": apresentante.get("CPFCNPJ"),
            "pessoa_vinculos": vinculos,
        }
        return map_titulo_index_row(mapped_row) or {}

    @staticmethod
    def _build_pagination_meta(page: int, per_page: int, total: int) -> dict[str, int]:
        total_pages = (total + per_page - 1) // per_page if per_page > 0 else 0
        return {
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": total_pages,
        }


def _mapping_or_empty(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _first_apresentante(vinculos: list[Any]) -> Mapping[str, Any]:
    for vinculo in vinculos:
        if not isinstance(vinculo, Mapping):
            continue
        tipo = str(vinculo.get("TIPO_VINCULO") or "").strip().upper()
        if tipo == "APRESENTANTE":
            return vinculo
    return {}


def _decimal_or_original(value: Any) -> Any:
    if isinstance(value, Decimal):
        return value
    if isinstance(value, str):
        normalized = value.strip().replace(",", ".")
        if not normalized:
            return value
        try:
            return Decimal(normalized)
        except InvalidOperation:
            return value
    return value


def _int_or_none(value: Any) -> int | None:
    normalized = _decimal_or_original(value)
    if normalized is None:
        return None
    try:
        return int(normalized)
    except (TypeError, ValueError):
        return None


def _decimal_or_none(value: str) -> Decimal | None:
    normalized = value.strip().replace(",", ".")
    if not normalized:
        return None
    try:
        return Decimal(normalized)
    except InvalidOperation:
        return None


def _numero_apontamento_or_none(value: str) -> Decimal | None:
    numeric_value = _decimal_or_none(value)
    if numeric_value is None:
        return None
    digits = len(numeric_value.as_tuple().digits)
    decimal_places = max(-numeric_value.as_tuple().exponent, 0)
    if digits > 10 or decimal_places > 2:
        return None
    return numeric_value


def _safe_like_pattern(value: str, max_length: int) -> str | None:
    text = value.strip()
    if not text or len(text) > max_length:
        return None
    if len(text) + 2 <= max_length:
        return f"%{text}%"
    return text

