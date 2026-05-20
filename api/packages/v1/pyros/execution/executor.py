from typing import Any, Iterator, Mapping

from sqlalchemy import text

from database.firebird import Firebird
from packages.v1.pyros.exceptions.errors import PyrosExecutionError
from packages.v1.pyros.execution.result_mapper import ResultMapper
from packages.v1.pyros.observability.sql_logger import SqlLogger, get_sql_logger


class PyrosExecutor:
    def __init__(self, logger: SqlLogger | None = None) -> None:
        self._logger = logger or get_sql_logger()
    def fetch_all(
        self,
        sql: str,
        params: dict[str, Any] | None = None,
        connection: Any | None = None,
    ) -> list[Mapping[str, Any]]:
        params = params or {}
        try:
            if connection is not None:
                result = connection.execute(text(sql), params)
                rows = ResultMapper.map_all(result)
                self._logger.log(
                    operation="select",
                    table=None,
                    sql=sql,
                    params=params,
                    rows=len(rows),
                    status="success",
                    elapsed_ms=0.0,
                )
                return rows

            engine = Firebird.get_engine()
            with engine.connect() as conn:
                result = conn.execute(text(sql), params)
                rows = ResultMapper.map_all(result)
                self._logger.log(
                    operation="select",
                    table=None,
                    sql=sql,
                    params=params,
                    rows=len(rows),
                    status="success",
                    elapsed_ms=0.0,
                )
                return rows
        except Exception as exc:
            self._logger.log(
                operation="select",
                table=None,
                sql=sql,
                params=params,
                rows=None,
                status="error",
                elapsed_ms=0.0,
            )
            raise PyrosExecutionError("Falha ao executar fetch_all no Pyros") from exc

    def fetch_one(
        self,
        sql: str,
        params: dict[str, Any] | None = None,
        connection: Any | None = None,
    ) -> Mapping[str, Any] | None:
        params = params or {}
        try:
            if connection is not None:
                result = connection.execute(text(sql), params)
                row = ResultMapper.map_one(result)
                self._logger.log(
                    operation="select",
                    table=None,
                    sql=sql,
                    params=params,
                    rows=1 if row is not None else 0,
                    status="success",
                    elapsed_ms=0.0,
                )
                return row

            engine = Firebird.get_engine()
            with engine.connect() as conn:
                result = conn.execute(text(sql), params)
                row = ResultMapper.map_one(result)
                self._logger.log(
                    operation="select",
                    table=None,
                    sql=sql,
                    params=params,
                    rows=1 if row is not None else 0,
                    status="success",
                    elapsed_ms=0.0,
                )
                return row
        except Exception as exc:
            self._logger.log(
                operation="select",
                table=None,
                sql=sql,
                params=params,
                rows=None,
                status="error",
                elapsed_ms=0.0,
            )
            raise PyrosExecutionError("Falha ao executar fetch_one no Pyros") from exc

    def execute(
        self,
        sql: str,
        params: dict[str, Any] | None = None,
        connection: Any | None = None,
    ) -> None:
        params = params or {}
        try:
            if connection is not None:
                connection.execute(text(sql), params)
                self._logger.log(
                    operation="other",
                    table=None,
                    sql=sql,
                    params=params,
                    rows=None,
                    status="success",
                    elapsed_ms=0.0,
                )
                return

            engine = Firebird.get_engine()
            with engine.begin() as conn:
                conn.execute(text(sql), params)
                self._logger.log(
                    operation="other",
                    table=None,
                    sql=sql,
                    params=params,
                    rows=None,
                    status="success",
                    elapsed_ms=0.0,
                )
        except Exception as exc:
            self._logger.log(
                operation="other",
                table=None,
                sql=sql,
                params=params,
                rows=None,
                status="error",
                elapsed_ms=0.0,
            )
            raise PyrosExecutionError("Falha ao executar comando no Pyros") from exc

    def execute_returning(
        self,
        sql: str,
        params: dict[str, Any] | None = None,
        connection: Any | None = None,
    ) -> Mapping[str, Any] | None:
        params = params or {}
        try:
            if connection is not None:
                result = connection.execute(text(sql), params)
                row = ResultMapper.map_one(result)
                self._logger.log(
                    operation="other",
                    table=None,
                    sql=sql,
                    params=params,
                    rows=1 if row is not None else 0,
                    status="success",
                    elapsed_ms=0.0,
                )
                return row

            engine = Firebird.get_engine()
            with engine.begin() as conn:
                result = conn.execute(text(sql), params)
                row = ResultMapper.map_one(result)
                self._logger.log(
                    operation="other",
                    table=None,
                    sql=sql,
                    params=params,
                    rows=1 if row is not None else 0,
                    status="success",
                    elapsed_ms=0.0,
                )
                return row
        except Exception as exc:
            self._logger.log(
                operation="other",
                table=None,
                sql=sql,
                params=params,
                rows=None,
                status="error",
                elapsed_ms=0.0,
            )
            raise PyrosExecutionError("Falha ao executar comando returning no Pyros") from exc

    def stream(
        self,
        sql: str,
        params: dict[str, Any] | None = None,
        chunk_size: int = 500,
        connection: Any | None = None,
    ) -> Iterator[Mapping[str, Any]]:
        if chunk_size <= 0:
            raise PyrosExecutionError("chunk_size deve ser maior que zero")

        params = params or {}
        try:
            if connection is not None:
                result = connection.execute(text(sql), params)
                rows = list(result.mappings().all())
                for row in rows:
                    yield row
                self._logger.log(
                    operation="select",
                    table=None,
                    sql=sql,
                    params=params,
                    rows=len(rows),
                    status="success",
                    elapsed_ms=0.0,
                )
                return

            engine = Firebird.get_engine()
            with engine.connect() as conn:
                result = conn.execute(text(sql), params)
                rows = list(result.mappings().all())
                for row in rows:
                    yield row
                self._logger.log(
                    operation="select",
                    table=None,
                    sql=sql,
                    params=params,
                    rows=len(rows),
                    status="success",
                    elapsed_ms=0.0,
                )
        except Exception as exc:
            self._logger.log(
                operation="select",
                table=None,
                sql=sql,
                params=params,
                rows=None,
                status="error",
                elapsed_ms=0.0,
            )
            raise PyrosExecutionError("Falha ao executar stream no Pyros") from exc
