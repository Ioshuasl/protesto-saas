from __future__ import annotations

from functools import lru_cache
from typing import Any, Type

from orm_py import DataTypes

from database.orm_firebird import get_orm

P_BANCO_TABLE = "P_BANCO"
P_BANCO_MODEL_NAME = "P_BANCO"

# Domínio Firebird; API — siglas S/N (g_banco_schema.py):
#   APONTAMENTO_PAG_POSTERIOR — S = sim, N/null = não
#   CUSTAS_NA_CONFIRMACAO — S = sim, N/null = não
#   LAYOUT_ID — FK P_LAYOUT

P_BANCO_ATTRIBUTES: dict[str, dict[str, Any]] = {
    "BANCO_ID": {
        "type": DataTypes.NUMERIC(10, 0),
        "primaryKey": True,
        "autoIncrement": False,
    },
    "CODIGO_BANCO": {"type": DataTypes.STRING(30), "allowNull": True},
    "DESCRICAO": {"type": DataTypes.STRING(60), "allowNull": True},
    "PESSOA_ID": {"type": DataTypes.NUMERIC(10, 0), "allowNull": True},
    "LAYOUT_ID": {"type": DataTypes.NUMERIC(10, 0), "allowNull": True},
    "APONTAMENTO_PAG_POSTERIOR": {"type": DataTypes.STRING(2), "allowNull": True},
    "CUSTAS_NA_CONFIRMACAO": {"type": DataTypes.STRING(2), "allowNull": True},
    "DEMAIS_DESPESAS": {"type": DataTypes.NUMERIC(10, 0), "allowNull": True},
}

P_BANCO_OPTIONS: dict[str, Any] = {
    "tableName": P_BANCO_TABLE,
    "primaryKey": "BANCO_ID",
}


@lru_cache(maxsize=1)
def get_p_banco_model() -> Type[Any]:
    orm = get_orm()

    existing = orm.models.get(P_BANCO_MODEL_NAME) or orm.models.get(P_BANCO_TABLE)
    if existing is not None:
        return existing

    return orm.define(
        P_BANCO_MODEL_NAME,
        P_BANCO_ATTRIBUTES,
        P_BANCO_OPTIONS,
    )
