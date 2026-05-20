from dataclasses import dataclass, field
from typing import Any, Literal


Direction = Literal["asc", "desc"]
Connector = Literal["and", "or"]


@dataclass(frozen=True, slots=True)
class FilterClause:
    field: str
    operator: str
    value: Any
    connector: Connector = "and"


@dataclass(frozen=True, slots=True)
class OrderClause:
    field: str
    direction: Direction = "asc"


@dataclass(frozen=True, slots=True)
class JoinClause:
    join_type: Literal["inner", "left"]
    table: str
    on: str
    alias: str | None = None


@dataclass(frozen=True, slots=True)
class RawClause:
    sql: str
    params: tuple[tuple[str, Any], ...] = field(default_factory=tuple)
    connector: Connector = "and"


@dataclass(frozen=True, slots=True)
class SelectQuery:
    table: str
    alias: str | None = None
    fields: tuple[str, ...] = field(default_factory=tuple)
    joins: tuple[JoinClause, ...] = field(default_factory=tuple)
    filters: tuple[FilterClause, ...] = field(default_factory=tuple)
    raw_filters: tuple[RawClause, ...] = field(default_factory=tuple)
    group_by: tuple[str, ...] = field(default_factory=tuple)
    having: tuple[FilterClause, ...] = field(default_factory=tuple)
    order_by: tuple[OrderClause, ...] = field(default_factory=tuple)
    limit: int | None = None
    offset: int | None = None
    is_count: bool = False
    allow_raw_sql: bool = False
