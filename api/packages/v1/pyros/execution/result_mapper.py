from typing import Any, Mapping


class ResultMapper:
    @staticmethod
    def map_all(result: Any) -> list[Mapping[str, Any]]:
        return list(result.mappings().all())

    @staticmethod
    def map_one(result: Any) -> Mapping[str, Any] | None:
        row = result.mappings().first()
        return row if row else None
