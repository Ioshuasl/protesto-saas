from __future__ import annotations

from functools import lru_cache
from typing import Any, Type

from orm_py import DataTypes

from database.orm_firebird import get_orm

P_LAYOUT_TABLE = "P_LAYOUT"
P_LAYOUT_MODEL_NAME = "P_LAYOUT"

P_LAYOUT_ATTRIBUTES: dict[str, dict[str, Any]] = {
    "LAYOUT_ID": {
        "type": DataTypes.NUMERIC(10, 0),
        "primaryKey": True,
        "autoIncrement": False,
    },
    "DESCRICAO": {"type": DataTypes.STRING(60), "allowNull": True},
}

P_LAYOUT_OPTIONS: dict[str, Any] = {
    "tableName": P_LAYOUT_TABLE,
    "primaryKey": "LAYOUT_ID",
}


@lru_cache(maxsize=1)
def get_p_layout_model() -> Type[Any]:
    orm = get_orm()

    existing = orm.models.get(P_LAYOUT_MODEL_NAME) or orm.models.get(P_LAYOUT_TABLE)
    if existing is not None:
        return existing

    return orm.define(
        P_LAYOUT_MODEL_NAME,
        P_LAYOUT_ATTRIBUTES,
        P_LAYOUT_OPTIONS,
    )
