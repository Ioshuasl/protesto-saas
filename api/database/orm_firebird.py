from __future__ import annotations

from dataclasses import asdict
from typing import Any, Mapping, Optional

from orm_py import OrmFirebird, normalize_firebird_charset, is_ansi_charset
from orm_py.schema.query_interface import QueryInterface

from actions.env.env_config_loader import EnvConfigLoader
from database.orm_firebird_settings import use_orm_firebird


def _build_connection_config() -> dict[str, Any]:
    env = EnvConfigLoader(".env")
    runtime_charset = normalize_firebird_charset(
        getattr(env, "ORIUS_API_FDB_CHARSET", None),
        default="UTF8",
    )
    driver_charset = "ISO8859_1" if is_ansi_charset(runtime_charset) else "UTF8"

    return {
        "host": env.ORIUS_API_FDB_HOST,
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


def get_orm() -> OrmFirebird:
    global _ORM_SINGLETON
    if _ORM_SINGLETON is not None:
        return _ORM_SINGLETON

    if not use_orm_firebird():
        raise RuntimeError(
            "ORM Firebird desabilitado. Defina USE_ORM_FIREBIRD=true no .env para usar orm-firebird-py."
        )
    orm = OrmFirebird(_build_connection_config())
    orm.authenticate()
    _ORM_SINGLETON = orm
    _register_administrativo_associations_once()
    return _ORM_SINGLETON


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


def describe_p_titulo_schema() -> dict[str, Any]:
    return describe_table_schema("P_TITULO")


def describe_g_tb_estadocivil_schema() -> dict[str, Any]:
    return describe_table_schema("G_TB_ESTADOCIVIL")


def describe_g_tb_profissao_schema() -> dict[str, Any]:
    return describe_table_schema("G_TB_PROFISSAO")


def describe_g_cidade_schema() -> dict[str, Any]:
    return describe_table_schema("G_CIDADE")
