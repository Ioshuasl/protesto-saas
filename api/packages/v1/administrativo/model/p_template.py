from __future__ import annotations

from functools import lru_cache
from typing import Any, Type

from orm_py import DataTypes

from database.orm_firebird import get_orm

P_TEMPLATE_TABLE = "P_TEMPLATE"
P_TEMPLATE_MODEL_NAME = "P_TEMPLATE"

# P_TEMPLATE - templates de texto do protesto.
# Firebird: NUMERICO = NUMERIC(10,2); TEXTO_BLOB = BLOB SUB_TYPE BINARY.

P_TEMPLATE_ATTRIBUTES: dict[str, dict[str, Any]] = {
    "TEMPLATE_ID": {
        "type": DataTypes.NUMERIC(10, 2),
        "primaryKey": True,
        "autoIncrement": False,
        "allowNull": False,
    },
    "DESCRICAO": {"type": DataTypes.STRING(60), "allowNull": False},
    "TEXTO": {"type": DataTypes.BLOB_BINARY(), "allowNull": True},
}

P_TEMPLATE_OPTIONS: dict[str, Any] = {
    "tableName": P_TEMPLATE_TABLE,
    "primaryKey": "TEMPLATE_ID",
}


@lru_cache(maxsize=1)
def get_p_template_model() -> Type[Any]:
    orm = get_orm()

    existing = orm.models.get(P_TEMPLATE_MODEL_NAME) or orm.models.get(P_TEMPLATE_TABLE)
    if existing is not None:
        return existing

    return orm.define(
        P_TEMPLATE_MODEL_NAME,
        P_TEMPLATE_ATTRIBUTES,
        P_TEMPLATE_OPTIONS,
    )
