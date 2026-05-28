from __future__ import annotations

from collections.abc import Callable
from dataclasses import asdict
from typing import Any, Mapping, Optional, TypeVar

from sqlalchemy import text

from orm_py import OrmFirebird, normalize_firebird_charset, is_ansi_charset
from orm_py.schema.query_interface import QueryInterface

from actions.env.env_config_loader import EnvConfigLoader
from database.firebird_host import resolve_firebird_host
from database.orm_firebird_settings import use_orm_firebird
from orm_py.errors import OrmFirebirdError


T = TypeVar("T")


def _is_transient_connection_error(exc: BaseException) -> bool:
    message = str(exc).lower()
    markers = (
        "unable to complete network request",
        "failed to establish a connection",
        "connection shutdown",
        "connection reset",
        "connection refused",
        "network is unreachable",
        "no route to host",
        "broken pipe",
    )
    return any(marker in message for marker in markers)


def is_firebird_connection_error(exc: BaseException) -> bool:
    if isinstance(exc, OrmFirebirdError):
        original = getattr(exc, "original_error", None)
        if original is not None:
            return _is_transient_connection_error(original)
    return _is_transient_connection_error(exc)


def reset_firebird_connections() -> None:
    from database.firebird import Firebird

    _dispose_orm_singleton()
    Firebird.dispose()


def run_with_firebird_retry(operation: Callable[[], T]) -> T:
    """
    Executa operação ORM/SQLAlchemy e, em falha transitória de rede com o
    Firebird, descarta pools antigos e tenta novamente uma vez.
    """
    last_error: BaseException | None = None
    for attempt in range(2):
        try:
            return operation()
        except Exception as exc:
            last_error = exc
            if attempt == 0 and is_firebird_connection_error(exc):
                reset_firebird_connections()
                continue
            raise

    if last_error is not None:
        raise last_error
    raise RuntimeError("run_with_firebird_retry: operação não retornou resultado.")


def _build_connection_config() -> dict[str, Any]:
    env = EnvConfigLoader(".env")
    runtime_charset = normalize_firebird_charset(
        getattr(env, "ORIUS_API_FDB_CHARSET", None),
        default="UTF8",
    )
    driver_charset = "ISO8859_1" if is_ansi_charset(runtime_charset) else "UTF8"

    return {
        "host": resolve_firebird_host(getattr(env, "ORIUS_API_FDB_HOST", None)),
        "port": int(env.ORIUS_API_FDB_PORT),
        "database": env.ORIUS_API_FDB_NAME,
        "user": env.ORIUS_API_FDB_USER,
        "password": env.ORIUS_API_FDB_PASSWORD,
        "charset": driver_charset,
        "pool_pre_ping": str(getattr(env, "ORIUS_API_FDB_POOL_PRE_PING", "true")).lower()
        in {"1", "true", "yes", "on"},
        "pool_size": int(getattr(env, "ORIUS_API_FDB_POOL_SIZE", None) or 5),
        "max_overflow": int(getattr(env, "ORIUS_API_FDB_POOL_MAX_OVERFLOW", None) or 10),
        "connect_args": {"charset": driver_charset},
    }


_ORM_SINGLETON: OrmFirebird | None = None
_FIREBIRD_DIALECT_PATCH_APPLIED = False


def ensure_firebird_dialect_patch() -> bool:
    """
    orm-firebird-py >= 0.1.2: corrige sqlalchemy_firebird VARCHAR bind cast
    (TypeError: int + str em _render_string_type) ao usar Op.like/eq em STRING.
    """
    global _FIREBIRD_DIALECT_PATCH_APPLIED
    if _FIREBIRD_DIALECT_PATCH_APPLIED:
        return True
    try:
        from orm_py.dialect_patch import apply_firebird_type_compiler_patch
    except ImportError:
        return False
    apply_firebird_type_compiler_patch()
    _FIREBIRD_DIALECT_PATCH_APPLIED = True
    return True


def firebird_orm_supports_string_where() -> bool:
    """Filtros ORM em colunas VARCHAR (LIKE/eq) exigem dialect_patch (0.1.2+)."""
    return ensure_firebird_dialect_patch()


def _dispose_orm_singleton() -> None:
    global _ORM_SINGLETON
    if _ORM_SINGLETON is None:
        return
    try:
        _ORM_SINGLETON.get_connection().get_engine().dispose()
    except Exception:
        pass
    _ORM_SINGLETON = None


def _orm_connection_is_alive(orm: OrmFirebird) -> bool:
    try:
        engine = orm.get_connection().get_engine()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1 FROM RDB$DATABASE"))
        return True
    except Exception as exc:
        if is_firebird_connection_error(exc):
            return False
        raise


def get_orm() -> OrmFirebird:
    global _ORM_SINGLETON
    if _ORM_SINGLETON is not None:
        if _orm_connection_is_alive(_ORM_SINGLETON):
            return _ORM_SINGLETON
        _dispose_orm_singleton()

    if not use_orm_firebird():
        raise RuntimeError(
            "ORM Firebird desabilitado. Defina USE_ORM_FIREBIRD=true no .env para usar orm-firebird-py."
        )
    ensure_firebird_dialect_patch()

    last_error: OrmFirebirdError | None = None
    for attempt in range(2):
        try:
            orm = OrmFirebird(_build_connection_config())
            orm.authenticate()
            _ORM_SINGLETON = orm
            _register_administrativo_associations_once()
            return _ORM_SINGLETON
        except OrmFirebirdError as exc:
            last_error = exc
            original = getattr(exc, "original_error", None) or exc
            if attempt == 0 and _is_transient_connection_error(original):
                _dispose_orm_singleton()
                continue
            raise

    if last_error is not None:
        raise last_error
    raise RuntimeError("Falha ao inicializar ORM Firebird.")


def _register_administrativo_associations_once() -> None:
    from packages.v1.administrativo.model.index import (
        register_administrativo_associations,
    )

    register_administrativo_associations()


def get_query_interface() -> QueryInterface:
    return QueryInterface(get_orm().get_connection())


def normalize_row_keys(row: Optional[Mapping[str, Any]]) -> Optional[dict[str, Any]]:
    if row is None:
        return None
    return {str(key).lower(): value for key, value in dict(row).items()}


def normalize_rows(rows: list[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [normalize_row_keys(row) or {} for row in rows]


def describe_table_schema(table_name: str) -> dict[str, Any]:
    """Schema tools — útil para debug (list_tables, describe_table, FKs)."""
    qi = get_query_interface()
    table = table_name.strip().upper()
    columns = qi.describe_table(table)
    foreign_keys = [
        asdict(fk)
        for fk in qi.list_foreign_keys()
        if fk.child_table == table or fk.parent_table == table
    ]
    return {
        "table": table,
        "exists": qi.table_exists(table),
        "columns": [asdict(column) for column in columns],
        "foreign_keys": foreign_keys,
    }


def describe_g_feriado_schema() -> dict[str, Any]:
    return describe_table_schema("G_FERIADO")


def describe_p_pessoa_schema() -> dict[str, Any]:
    return describe_table_schema("P_PESSOA")


def describe_p_pessoa_vinculo_schema() -> dict[str, Any]:
    return describe_table_schema("P_PESSOA_VINCULO")


def describe_p_titulo_schema() -> dict[str, Any]:
    return describe_table_schema("P_TITULO")


def describe_g_tb_estadocivil_schema() -> dict[str, Any]:
    return describe_table_schema("G_TB_ESTADOCIVIL")


def describe_g_tb_profissao_schema() -> dict[str, Any]:
    return describe_table_schema("G_TB_PROFISSAO")


def describe_g_cidade_schema() -> dict[str, Any]:
    return describe_table_schema("G_CIDADE")
