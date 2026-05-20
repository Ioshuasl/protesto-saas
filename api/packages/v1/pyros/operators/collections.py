from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class In:
    value: list[object] | tuple[object, ...]

    operator = "IN"
