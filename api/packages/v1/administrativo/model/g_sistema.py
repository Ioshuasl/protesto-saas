from __future__ import annotations

from functools import lru_cache
from typing import Any, Type

from orm_py import DataTypes

from database.orm_firebird import get_orm

G_SISTEMA_TABLE = "G_SISTEMA"
G_SISTEMA_MODEL_NAME = "G_SISTEMA"

G_SISTEMA_ATTRIBUTES: dict[str, dict[str, Any]] = {
    "SISTEMA_ID": {
        "type": DataTypes.NUMERIC(10, 2),
        "primaryKey": True,
        "autoIncrement": False,
        "allowNull": False,
    },
    "DESCRICAO": {"type": DataTypes.STRING(30), "allowNull": True},
    "SITUACAO": {"type": DataTypes.STRING(1), "allowNull": True},
    "TIPO_CARTORIO": {"type": DataTypes.STRING(3), "allowNull": True},
    "VERSAO": {"type": DataTypes.STRING(15), "allowNull": True},
    "DATA_VERSAO": {"type": DataTypes.TIMESTAMP(), "allowNull": True},
    "NOME_EXE": {"type": DataTypes.STRING(30), "allowNull": True},
}

G_SISTEMA_OPTIONS: dict[str, Any] = {
    "tableName": G_SISTEMA_TABLE,
    "primaryKey": "SISTEMA_ID",
}


@lru_cache(maxsize=1)
def get_g_sistema_model() -> Type[Any]:
    orm = get_orm()

    existing = orm.models.get(G_SISTEMA_MODEL_NAME) or orm.models.get(G_SISTEMA_TABLE)
    if existing is not None:
        return existing

    return orm.define(
        G_SISTEMA_MODEL_NAME,
        G_SISTEMA_ATTRIBUTES,
        G_SISTEMA_OPTIONS,
    )
