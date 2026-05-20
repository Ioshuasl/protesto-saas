from __future__ import annotations
from dataclasses import dataclass
from typing import Any, ClassVar, List, Mapping, TypedDict
from collections.abc import Mapping as MappingABC

from fastapi import Request


class PaginationDict(TypedDict):
    page: int
    per_page: int


class SortDict(TypedDict):
    field: str
    direction: str


class FilterDict(TypedDict):
    field: str
    operator: str
    value: str


class QueryParamsDict(TypedDict):
    pagination: PaginationDict
    sort: SortDict | None
    filters: List[FilterDict]


@dataclass(slots=True)
class Pagination:
    page: int
    per_page: int


@dataclass(slots=True)
class Sort:
    field: str
    direction: str


@dataclass(slots=True)
class Filter:
    field: str
    operator: str
    value: str


@dataclass(slots=True)
class QueryParams(MappingABC[str, Any]):
    """
    Estrutura de alto nível para acesso a query params.

    - Acesso por atributo (recomendado):
        qp.page, qp.per_page, qp.pagination, qp.sort, qp.filters
    - Acesso por chave (compatibilidade):
        qp["pagination"], qp["sort"], qp["filters"]
    """

    pagination: Pagination
    sort: Sort | None
    filters: List[Filter]

    # ------ Propriedades de conveniência (flatten de paginação) ------
    @property
    def page(self) -> int:
        raw_value = getattr(self.pagination, "page", None)
        return QueryParamsParser._safe_int(raw_value, default=1, min_value=1)

    @property
    def per_page(self) -> int:
        raw_value = getattr(self.pagination, "per_page", None)
        return QueryParamsParser._safe_int(
            raw_value,
            default=QueryParamsParser.DEFAULT_PER_PAGE,
            min_value=1,
        )

    # ------ Implementação Mapping para compatibilidade ------
    def __getitem__(self, key: str) -> Any:  # type: ignore[override]
        if key == "pagination":
            return self.pagination
        if key == "sort":
            return self.sort
        if key == "filters":
            return self.filters
        raise KeyError(key)

    def __iter__(self):  # type: ignore[override]
        return iter(("pagination", "sort", "filters"))

    def __len__(self) -> int:  # type: ignore[override]
        return 3

    def to_dict(self) -> QueryParamsDict:
        """Representação em dict simples (útil para serialização/log)."""
        return {
            "pagination": {
                "page": self.pagination.page,
                "per_page": self.pagination.per_page,
            },
            "sort": (
                {
                    "field": self.sort.field,
                    "direction": self.sort.direction,
                }
                if self.sort
                else None
            ),
            "filters": [
                {
                    "field": f.field,
                    "operator": f.operator,
                    "value": f.value,
                }
                for f in self.filters
            ],
        }


@dataclass(slots=True)
class QueryParamsParser:
    """Helper estático para converter query_params do FastAPI em estrutura normalizada."""

    # ClassVar evita que o atributo vire field/slot de dataclass,
    # garantindo que seja apenas um inteiro normal em nível de classe.
    DEFAULT_PER_PAGE: ClassVar[int] = 20

    @staticmethod
    async def parse(request: Request) -> QueryParams:
        """
        Converte diretamente um Request do FastAPI na estrutura normalizada de query params.
        """
        return QueryParamsParser._from_query_params(request.query_params)

    @staticmethod
    def _from_query_params(query_params: Mapping[str, str]) -> QueryParams:
        """
        Converte Request.query_params (FastAPI) na estrutura:
        {
        "pagination": { "page": int, "per_page": int },
        "sort": { "field": str, "direction": str } | None,
        "filters": [ { "field": str, "operator": str, "value": str }, ... ]
        }
        """
        pagination = QueryParamsParser._parse_pagination(query_params)
        sort = QueryParamsParser._parse_sort(query_params)
        filters = QueryParamsParser._parse_filters(query_params)
        return QueryParams(
            pagination=pagination,
            sort=sort,
            filters=filters,
        )

    @staticmethod
    def _parse_pagination(query_params: Mapping[str, str]) -> Pagination:
        raw_page = query_params.get("p")
        page = QueryParamsParser._safe_int(raw_page, default=1, min_value=1)

        raw_per_page = query_params.get("per_page") or query_params.get("perPage")
        per_page = QueryParamsParser._safe_int(
            raw_per_page,
            default=QueryParamsParser.DEFAULT_PER_PAGE,
            min_value=1,
        )
        return Pagination(page=page, per_page=per_page)

    @staticmethod
    def _parse_sort(query_params: Mapping[str, str]) -> Sort | None:
        """
        sort=pessoa_id.desc  ->  {"field": "pessoa_id", "direction": "desc"}
        """
        raw_sort = query_params.get("sort")
        if not raw_sort:
            return None
        parts = raw_sort.split(".", maxsplit=1)
        field = parts[0].strip()
        direction = parts[1].strip().lower() if len(parts) == 2 else "asc"
        if direction not in {"asc", "desc"}:
            direction = "asc"
        return Sort(field=field, direction=direction)

    @staticmethod
    def _parse_filters(query_params: Mapping[str, str]) -> List[Filter]:
        """
        f=pessoa_tipo:eq:F  ->  {"field": "pessoa_tipo", "operator": "eq", "value": "F"}
        Aceita múltiplos parâmetros f=... (usando getlist se existir).
        """
        result: List[Filter] = []
        # FastAPI / Starlette: QueryParams tem getlist("f")
        if hasattr(query_params, "getlist"):
            raw_filters = list(query_params.getlist("f"))  # type: ignore[attr-defined]
        else:
            # fallback caso seja apenas um dict normal
            raw = query_params.get("f")
            raw_filters = [raw] if raw is not None else []
        for raw in raw_filters:
            if not raw:
                continue
            # formato esperado: campo:op:valor
            parts = raw.split(":", maxsplit=2)
            if len(parts) != 3:
                # ignora filtros inválidos (poderia lançar erro se preferir)
                continue
            field, operator, value = (p.strip() for p in parts)
            if not field or not operator:
                continue
            result.append(Filter(field=field, operator=operator, value=value))
        return result

    @staticmethod
    def _safe_int(raw: Any, default: int, min_value: int | None = None) -> int:
        try:
            value = int(raw)
        except (TypeError, ValueError):
            return default
        if min_value is not None and value < min_value:
            return default
        return value
