from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Equals:
    value: object

    operator = "="


@dataclass(frozen=True, slots=True)
class Like:
    value: object

    operator = "LIKE"
