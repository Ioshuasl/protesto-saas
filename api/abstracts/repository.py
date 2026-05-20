import asyncio
import base64
import json
import logging
import re
import weakref
from datetime import date, datetime, timezone
from pathlib import Path
from threading import Thread
from typing import Any, List, Literal, Mapping, Optional, Union, overload, cast
from uuid import uuid4

from sqlalchemy import text
from sqlalchemy.engine import Connection, CursorResult
from sqlalchemy.exc import SQLAlchemyError

from database.firebird import Firebird

logger = logging.getLogger(__name__)

_ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_ISO_DATETIME_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2}(?:\.\d+)?)?(?:Z|[+-]\d{2}:\d{2})?$"
)


class AttrDict(dict):
    """
    Dicionario com acesso via atributo.
    Compativel com **row e row.campo.
    """

    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError as exc:
            raise AttributeError(item) from exc

    def __setattr__(self, key, value):
        self[key] = value


class _ManagedCursorResult:
    """
    Wrapper explicito para manter a conexao viva enquanto o resultado estiver em uso.
    Preserva a interface pratica do CursorResult sem monkey patch no objeto do SQLAlchemy.
    """

    def __init__(self, conn: Connection, result: CursorResult[Any]) -> None:
        self._conn = conn
        self._result = result
        self._finalizer = weakref.finalize(self, self._safe_close_connection)

    def _safe_close_connection(self) -> None:
        if not self._conn.closed:
            self._conn.close()

    def close(self) -> None:
        try:
            self._result.close()
        finally:
            if self._finalizer.alive:
                self._finalizer()

    def __iter__(self):
        return iter(self._result)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def __getattr__(self, item: str) -> Any:
        return getattr(self._result, item)


class BaseRepository:
    def __init__(self, blob_in_base64: bool = True):
        self._blob_in_base64 = blob_in_base64
        self._sql_log_dir = Path(__file__).resolve().parents[1] / "storage" / "logs" / "sqls"

    @overload
    def _execute(
        self,
        sql: str,
        params: Optional[dict[str, Any]],
        fetch: Literal["all"],
        connection: Optional[Connection] = None,
    ) -> List[Mapping[str, Any]]: ...

    @overload
    def _execute(
        self,
        sql: str,
        params: Optional[dict[str, Any]],
        fetch: Literal["one"],
        connection: Optional[Connection] = None,
    ) -> Optional[Mapping[str, Any]]: ...

    @overload
    def _execute(
        self,
        sql: str,
        params: Optional[dict[str, Any]],
        fetch: Literal["none"],
        connection: Optional[Connection] = None,
    ) -> None: ...

    @overload
    def _execute(
        self,
        sql: str,
        params: Optional[dict[str, Any]],
        fetch: Literal["result"],
        connection: Optional[Connection] = None,
    ) -> CursorResult[Any]: ...

    def _materialize_blob(self, value: Any) -> Any:
        if value is None:
            return None

        if isinstance(value, (bytes, bytearray)):
            if self._blob_in_base64:
                return base64.b64encode(value).decode("ascii")
            return value

        if hasattr(value, "read") and callable(value.read):
            try:
                raw = value.read()
            except AttributeError:
                logger.warning("BLOB reader invalido (handle ausente); retornando None")
                return None
            except Exception:
                logger.exception("Falha ao materializar BLOB via stream")
                raise

            if self._blob_in_base64 and raw is not None:
                return base64.b64encode(raw).decode("ascii")
            return raw

        return value

    def _normalize_param_value(self, value: Any) -> Any:
        if isinstance(value, str):
            candidate = value.strip()
            if _ISO_DATE_RE.match(candidate):
                try:
                    return date.fromisoformat(candidate)
                except ValueError:
                    return value
            if _ISO_DATETIME_RE.match(candidate):
                try:
                    if candidate.endswith("Z"):
                        candidate = f"{candidate[:-1]}+00:00"
                    parsed = datetime.fromisoformat(candidate)
                    if parsed.tzinfo is not None:
                        parsed = parsed.astimezone(timezone.utc).replace(tzinfo=None)
                    return parsed
                except ValueError:
                    return value
        if isinstance(value, list):
            return [self._normalize_param_value(item) for item in value]
        if isinstance(value, tuple):
            return tuple(self._normalize_param_value(item) for item in value)
        if isinstance(value, dict):
            return {k: self._normalize_param_value(v) for k, v in value.items()}
        return value

    def _normalize_params(self, params: Optional[dict[str, Any]]) -> Optional[dict[str, Any]]:
        if not params:
            return params
        return {key: self._normalize_param_value(value) for key, value in params.items()}

    def _normalize_row(self, row: Mapping[str, Any]) -> Mapping[str, Any]:
        data = AttrDict()

        for key, value in row.items():
            data[key] = self._materialize_blob(value)

        return data

    def _normalize_all(self, result: CursorResult[Any]) -> List[Mapping[str, Any]]:
        normalized: List[Mapping[str, Any]] = []
        for row in result:
            mapping = dict(row._mapping)
            normalized.append(self._normalize_row(mapping))
        return normalized

    def _normalize_one(self, result: CursorResult[Any]) -> Optional[Mapping[str, Any]]:
        row = result.fetchone()
        if not row:
            return None
        mapping = dict(row._mapping)
        return self._normalize_row(mapping)

    def _log_sql_error(
        self,
        error: SQLAlchemyError,
        fetch: Literal["all", "one", "none", "result"],
    ) -> None:
        logger.exception(
            "Erro SQL no repository",
            extra={
                "repository": self.__class__.__name__,
                "fetch": fetch,
                "error_type": error.__class__.__name__,
            },
        )

    async def _save_executed_sql_log(
        self,
        sql: str,
        params: Optional[dict[str, Any]],
        fetch: Literal["all", "one", "none", "result"],
        status: Literal["success", "error"],
        error: Optional[str] = None,
    ) -> None:
        payload = {
            "id": uuid4().hex,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "repository": self.__class__.__name__,
            "fetch": fetch,
            "status": status,
            "sql": sql,
            "params": params or {},
            "error": error,
        }

        await asyncio.to_thread(self._write_sql_log_file, payload)

    def _write_sql_log_file(self, payload: dict[str, Any]) -> None:
        self._sql_log_dir.mkdir(parents=True, exist_ok=True)
        file_path = self._sql_log_dir / f"{payload['timestamp'][:10]}_{payload['id']}.json"
        file_path.write_text(
            json.dumps(payload, ensure_ascii=True, default=str, indent=2),
            encoding="utf-8",
        )

    def _schedule_sql_log(
        self,
        sql: str,
        params: Optional[dict[str, Any]],
        fetch: Literal["all", "one", "none", "result"],
        status: Literal["success", "error"],
        error: Optional[str] = None,
    ) -> None:
        coroutine = self._save_executed_sql_log(sql, params, fetch, status, error)

        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            Thread(target=lambda: asyncio.run(coroutine), daemon=True).start()
            return

        loop.create_task(coroutine)

    def _execute_read(
        self,
        sql: str,
        params: Optional[dict[str, Any]],
        fetch: Literal["all", "one"],
        connection: Optional[Connection] = None,
    ) -> Union[List[Mapping[str, Any]], Optional[Mapping[str, Any]]]:
        if connection is not None:
            result = connection.execute(text(sql), self._normalize_params(params) or {})

            if fetch == "all":
                return self._normalize_all(result)

            return self._normalize_one(result)

        engine = Firebird.get_engine()
        with engine.connect() as conn:
            result = conn.execute(text(sql), params or {})

            if fetch == "all":
                return self._normalize_all(result)

            return self._normalize_one(result)

    def _execute_write(
        self,
        sql: str,
        params: Optional[dict[str, Any]],
        fetch: Literal["none", "one"],
        connection: Optional[Connection] = None,
    ) -> Optional[Mapping[str, Any]]:
        if connection is not None:
            normalized_params = self._normalize_params(params) or {}
            result = connection.execute(text(sql), normalized_params)

            if fetch == "one":
                return self._normalize_one(result)

            return None

        engine = Firebird.get_engine()
        with engine.begin() as conn:
            normalized_params = self._normalize_params(params) or {}
            result = conn.execute(text(sql), normalized_params)

            if fetch == "one":
                return self._normalize_one(result)

            return None

    def _execute_result(
        self,
        sql: str,
        params: Optional[dict[str, Any]],
        connection: Optional[Connection] = None,
    ) -> CursorResult[Any]:
        if connection is not None:
            return connection.execute(text(sql), self._normalize_params(params) or {})

        engine = Firebird.get_engine()
        conn = engine.connect()

        try:
            result = conn.execute(text(sql), params or {})
        except SQLAlchemyError:
            conn.close()
            raise
        except Exception:
            conn.close()
            raise

        managed_result = _ManagedCursorResult(conn, result)
        return cast(CursorResult[Any], managed_result)

    def _execute(
        self,
        sql: str,
        params: Optional[dict[str, Any]] = None,
        fetch: Literal["all", "one", "none", "result"] = "result",
        connection: Optional[Connection] = None,
    ) -> Union[
        List[Mapping[str, Any]],
        Optional[Mapping[str, Any]],
        None,
        CursorResult[Any],
    ]:
        try:
            if fetch == "result":
                response = self._execute_result(sql, params, connection=connection)
                self._schedule_sql_log(sql, params, fetch, status="success")
                return response

            if fetch == "all":
                response = self._execute_read(sql, params, fetch="all", connection=connection)
                self._schedule_sql_log(sql, params, fetch, status="success")
                return response

            if fetch == "one":
                response = self._execute_read(sql, params, fetch="one", connection=connection)
                self._schedule_sql_log(sql, params, fetch, status="success")
                return response

            response = self._execute_write(sql, params, fetch="none", connection=connection)
            self._schedule_sql_log(sql, params, fetch, status="success")
            return response
        except SQLAlchemyError as exc:
            self._schedule_sql_log(sql, params, fetch, status="error", error=str(exc))
            self._log_sql_error(exc, fetch)
            raise

    def query(
        self,
        sql: str,
        params: Optional[dict[str, Any]] = None,
        connection: Optional[Connection] = None,
    ) -> CursorResult[Any]:
        return self._execute(sql, params, fetch="result", connection=connection)

    def fetch_all(
        self,
        sql: str,
        params: Optional[dict[str, Any]] = None,
        connection: Optional[Connection] = None,
    ) -> List[Mapping[str, Any]]:
        return self._execute(sql, params, fetch="all", connection=connection)

    def fetch_one(
        self,
        sql: str,
        params: Optional[dict[str, Any]] = None,
        connection: Optional[Connection] = None,
    ) -> Optional[Mapping[str, Any]]:
        return self._execute(sql, params, fetch="one", connection=connection)

    def run(
        self,
        sql: str,
        params: Optional[dict[str, Any]] = None,
        connection: Optional[Connection] = None,
    ) -> None:
        self._execute(sql, params, fetch="none", connection=connection)

    def run_and_return(
        self,
        sql: str,
        params: Optional[dict[str, Any]] = None,
        connection: Optional[Connection] = None,
    ) -> Optional[Mapping[str, Any]]:
        try:
            if connection is not None:
                normalized_params = self._normalize_params(params) or {}
                result = connection.execute(text(sql), normalized_params)
                self._schedule_sql_log(sql, params, fetch="one", status="success")
                return self._normalize_one(result)

            response = self._execute_write(sql, params, fetch="one")
            self._schedule_sql_log(sql, params, fetch="one", status="success")
            return response
        except SQLAlchemyError as exc:
            self._schedule_sql_log(sql, params, fetch="one", status="error", error=str(exc))
            self._log_sql_error(exc, fetch="one")
            raise
