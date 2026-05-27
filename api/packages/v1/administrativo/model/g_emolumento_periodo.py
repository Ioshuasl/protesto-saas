from __future__ import annotations

from functools import lru_cache
from typing import Any, Type

from orm_py import DataTypes

from database.orm_firebird import get_orm

G_EMOLUMENTO_PERIODO_TABLE = "G_EMOLUMENTO_PERIODO"
G_EMOLUMENTO_PERIODO_MODEL_NAME = "G_EMOLUMENTO_PERIODO"

G_EMOLUMENTO_PERIODO_ATTRIBUTES: dict[str, dict[str, Any]] = {
    "EMOLUMENTO_PERIODO_ID": {
        "type": DataTypes.NUMERIC(10, 2),
        "primaryKey": True,
        "autoIncrement": False,
        "allowNull": False,
    },
    "DESCRICAO": {"type": DataTypes.STRING(60), "allowNull": True},
    "SITUACAO": {"type": DataTypes.STRING(1), "allowNull": True},
    "DATA_INICIAL": {"type": DataTypes.TIMESTAMP(), "allowNull": True},
}

G_EMOLUMENTO_PERIODO_OPTIONS: dict[str, Any] = {
    "tableName": G_EMOLUMENTO_PERIODO_TABLE,
    "primaryKey": "EMOLUMENTO_PERIODO_ID",
}


@lru_cache(maxsize=1)
def get_g_emolumento_periodo_model() -> Type[Any]:
    orm = get_orm()

    existing = orm.models.get(G_EMOLUMENTO_PERIODO_MODEL_NAME) or orm.models.get(
        G_EMOLUMENTO_PERIODO_TABLE
    )
    if existing is not None:
        return existing

    return orm.define(
        G_EMOLUMENTO_PERIODO_MODEL_NAME,
        G_EMOLUMENTO_PERIODO_ATTRIBUTES,
        G_EMOLUMENTO_PERIODO_OPTIONS,
    )
