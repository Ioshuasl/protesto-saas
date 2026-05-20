from __future__ import annotations

import hashlib
import time
from dataclasses import dataclass
from typing import Any, Literal


Status = Literal["success", "error"]
Operation = Literal["select", "insert", "update", "delete", "other"]


def _fingerprint(sql: str) -> str:
    normalized = " ".join(sql.split()).strip().lower()
    return hashlib.sha1(normalized.encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class SqlEvent:
    operation: Operation
    table: str | None
    sql: str
    params_count: int
    rows: int | None
    status: Status
    elapsed_ms: float
    fingerprint: str
    slow: bool


class SqlLogger:
    def __init__(self, slow_threshold_ms: float = 300.0) -> None:
        self._slow_threshold_ms = slow_threshold_ms
        self._events: list[SqlEvent] = []

    @property
    def events(self) -> list[SqlEvent]:
        return list(self._events)

    def log(
        self,
        *,
        operation: Operation,
        table: str | None,
        sql: str,
        params: dict[str, Any],
        rows: int | None,
        status: Status,
        elapsed_ms: float,
    ) -> None:
        event = SqlEvent(
            operation=operation,
            table=table,
            sql=sql,
            params_count=len(params),
            rows=rows,
            status=status,
            elapsed_ms=elapsed_ms,
            fingerprint=_fingerprint(sql),
            slow=elapsed_ms >= self._slow_threshold_ms,
        )
        self._events.append(event)

    def timed(
        self,
        *,
        operation: Operation,
        table: str | None,
        sql: str,
        params: dict[str, Any],
        rows_getter: callable | None = None,
    ):
        start = time.perf_counter()
        try:
            result = yield
            rows = rows_getter(result) if rows_getter is not None else None
            elapsed_ms = (time.perf_counter() - start) * 1000
            self.log(
                operation=operation,
                table=table,
                sql=sql,
                params=params,
                rows=rows,
                status="success",
                elapsed_ms=elapsed_ms,
            )
            return result
        except Exception:
            elapsed_ms = (time.perf_counter() - start) * 1000
            self.log(
                operation=operation,
                table=table,
                sql=sql,
                params=params,
                rows=None,
                status="error",
                elapsed_ms=elapsed_ms,
            )
            raise


_global_logger: SqlLogger | None = None


def get_sql_logger() -> SqlLogger:
    global _global_logger
    if _global_logger is None:
        _global_logger = SqlLogger()
    return _global_logger


def set_sql_logger(logger: SqlLogger | None) -> None:
    global _global_logger
    _global_logger = logger
