from __future__ import annotations

from functools import lru_cache
from typing import Any, Type

from orm_py import DataTypes

from database.orm_firebird import get_orm

G_CIDADE_TABLE = "G_CIDADE"
G_CIDADE_MODEL_NAME = "G_CIDADE"

# G_CIDADE — cidades (IBGE)
# Gerado a partir de QueryInterface.describe_table (Firebird santarita).

G_CIDADE_ATTRIBUTES: dict[str, dict[str, Any]] = {
    "CIDADE_ID": {"type": DataTypes.NUMERIC(10, 0), "primaryKey": True, "autoIncrement": False, "allowNull": False},
    "UF": {"type": DataTypes.STRING(3), "allowNull": True},
    "CIDADE_NOME": {"type": DataTypes.STRING(150), "allowNull": True},
    "CODIGO_IBGE": {"type": DataTypes.STRING(10), "allowNull": True},
    "CODIGO_GYN": {"type": DataTypes.STRING(10), "allowNull": True},
}

G_CIDADE_OPTIONS: dict[str, Any] = {
    "tableName": G_CIDADE_TABLE,
    "primaryKey": "CIDADE_ID",
}


@lru_cache(maxsize=1)
def get_g_cidade_model() -> Type[Any]:
    orm = get_orm()

    existing = orm.models.get(G_CIDADE_MODEL_NAME) or orm.models.get(G_CIDADE_TABLE)
    if existing is not None:
        return existing

    return orm.define(
        G_CIDADE_MODEL_NAME,
        G_CIDADE_ATTRIBUTES,
        G_CIDADE_OPTIONS,
    )
