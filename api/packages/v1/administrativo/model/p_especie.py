from __future__ import annotations

from functools import lru_cache
from typing import Any, Type

from orm_py import DataTypes

from database.orm_firebird import get_orm

P_ESPECIE_TABLE = "P_ESPECIE"
P_ESPECIE_MODEL_NAME = "P_ESPECIE"

# P_ESPECIE — cadastro de espécies de título (sigla FEBRABAN/CRA, até 3 caracteres)

P_ESPECIE_ATTRIBUTES: dict[str, dict[str, Any]] = {
    "ESPECIE_ID": {
        "type": DataTypes.NUMERIC(10, 2),
        "primaryKey": True,
        "autoIncrement": False,
    },
    "ESPECIE": {"type": DataTypes.STRING(3), "allowNull": True},
    "DESCRICAO": {"type": DataTypes.STRING(260), "allowNull": True},
}

P_ESPECIE_OPTIONS: dict[str, Any] = {
    "tableName": P_ESPECIE_TABLE,
    "primaryKey": "ESPECIE_ID",
}


@lru_cache(maxsize=1)
def get_p_especie_model() -> Type[Any]:
    orm = get_orm()

    existing = orm.models.get(P_ESPECIE_MODEL_NAME) or orm.models.get(P_ESPECIE_TABLE)
    if existing is not None:
        return existing

    return orm.define(
        P_ESPECIE_MODEL_NAME,
        P_ESPECIE_ATTRIBUTES,
        P_ESPECIE_OPTIONS,
    )
