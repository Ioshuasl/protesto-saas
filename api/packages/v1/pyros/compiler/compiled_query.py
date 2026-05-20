from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class CompiledQuery:
    sql: str
    params: dict[str, Any] = field(default_factory=dict)
