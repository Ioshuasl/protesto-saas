from __future__ import annotations

from typing import Any
from collections.abc import Mapping

from orm_py import Op

from abstracts.repository import BaseRepository
from actions.data.query_params_parser import QueryParams
from packages.v1.administrativo.model.g_emolumento_item import get_g_emolumento_item_model
from packages.v1.administrativo.model.index import register_administrativo_associations
from packages.v1.administrativo.schemas.g_emolumento_item_schema import (
    GEmolumentoItemListDetailsSchema,
)


class GEmolumentoItemListDetailsRepository(BaseRepository):
    _SORT_FIELD_MAP = {
        "emolumento_item_id": "EMOLUMENTO_ITEM_ID",
        "selo_grupo_id": "SELO_GRUPO_ID",
    }

    def execute(
        self, data: GEmolumentoItemListDetailsSchema, query_params: QueryParams
    ) -> dict[str, Any]:
        register_administrativo_associations()

        page = query_params.page
        per_page = query_params.per_page
        sort_field, sort_direction = self._resolve_sort(query_params)

        where = self._build_where(data)

        offset = (page - 1) * per_page
        options: dict[str, Any] = {
            "order": [(sort_field, sort_direction.upper())],
            "limit": per_page,
            "offset": offset,
            "include": self._build_includes(
                requires_emolumento=data.sistema_id is not None,
            ),
        }
        if where:
            options["where"] = where

        result = get_g_emolumento_item_model().findAndCountAll(options)
        total = int(result.get("count") or 0)
        rows = result.get("rows") or []
        normalized_rows = [
            self._normalize_payload(row)
            for row in rows
            if GEmolumentoItemListDetailsRepository._is_valid_list_row(row)
        ]

        return {
            "rows": normalized_rows,
            "pagination": self._build_pagination_meta(page, per_page, total),
        }

    @classmethod
    def _resolve_sort(cls, query_params: QueryParams) -> tuple[str, str]:
        sort = query_params.sort
        if sort is not None and sort.field:
            logical_field = sort.field.strip().lower()
            direction = sort.direction if sort.direction in {"asc", "desc"} else "asc"
            if logical_field in cls._SORT_FIELD_MAP:
                return cls._SORT_FIELD_MAP[logical_field], direction

        return "SELO_GRUPO_ID", "asc"

    @staticmethod
    def _has_busca(data: GEmolumentoItemListDetailsSchema) -> bool:
        return bool(data.busca and data.busca.strip())

    @classmethod
    def _build_selo_grupo_where(cls, data: GEmolumentoItemListDetailsSchema) -> dict[str, Any] | None:
        if not cls._has_busca(data):
            return None

        term = f"%{data.busca.strip()}%"
        return {
            Op.or_: [
                {"DESCRICAO": {Op.like: term}},
                {"NUMERO": {Op.like: term}},
            ]
        }

    @staticmethod
    def _build_required_item_filters() -> dict[str, Any]:
        return {
            Op.and_: [
                {"EMOLUMENTO_ITEM_ID": {Op.ne: None}},
                {"SELO_GRUPO_ID": {Op.ne: None}},
            ]
        }

    @staticmethod
    def _is_valid_list_row(row: Any) -> bool:
        if not isinstance(row, Mapping):
            return False

        item_id = row.get("EMOLUMENTO_ITEM_ID")
        if item_id is None:
            item_id = row.get("emolumento_item_id")
        if item_id is None:
            return False

        selo_grupo_id = row.get("SELO_GRUPO_ID")
        if selo_grupo_id is None:
            selo_grupo_id = row.get("selo_grupo_id")
        return selo_grupo_id is not None

    @staticmethod
    def _build_where(data: GEmolumentoItemListDetailsSchema) -> dict[str, Any]:
        clauses: list[dict[str, Any]] = [
            GEmolumentoItemListDetailsRepository._build_required_item_filters(),
        ]

        if data.emolumento_periodo_id is not None:
            clauses.append({"EMOLUMENTO_PERIODO_ID": data.emolumento_periodo_id})

        if data.sistema_id is not None:
            clauses.append({"emolumento": {"SISTEMA_ID": data.sistema_id}})

        selo_grupo_where = GEmolumentoItemListDetailsRepository._build_selo_grupo_where(data)
        if selo_grupo_where is not None:
            clauses.append({"selo_grupo": selo_grupo_where})

        if not clauses:
            return {}
        if len(clauses) == 1:
            return clauses[0]
        return {Op.and_: clauses}

    @staticmethod
    def _build_includes(requires_emolumento: bool) -> list[dict[str, Any]]:
        return [
            {
                "association": "selo_grupo",
                "required": True,
            },
            {
                "association": "emolumento",
                "required": requires_emolumento,
            },
        ]

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
    def _normalize_payload(value: Any) -> Any:
        if isinstance(value, Mapping):
            return {
                str(key).lower(): GEmolumentoItemListDetailsRepository._normalize_payload(
                    child
                )
                for key, child in dict(value).items()
            }
        if isinstance(value, list):
            return [
                GEmolumentoItemListDetailsRepository._normalize_payload(item)
                for item in value
            ]
        return value
