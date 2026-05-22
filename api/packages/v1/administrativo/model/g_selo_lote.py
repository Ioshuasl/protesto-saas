from __future__ import annotations

from functools import lru_cache
from typing import Any, Type

from orm_py import DataTypes

from database.orm_firebird import get_orm

G_SELO_LOTE_TABLE = "G_SELO_LOTE"
G_SELO_LOTE_MODEL_NAME = "G_SELO_LOTE"

# G_SELO_LOTE — lotes de selos
# FK: SELO_GRUPO_ID → G_SELO_GRUPO

G_SELO_LOTE_ATTRIBUTES: dict[str, dict[str, Any]] = {
    "SELO_LOTE_ID": {
        "type": DataTypes.NUMERIC(10, 2),
        "primaryKey": True,
        "autoIncrement": False,
        "allowNull": False,
    },
    "NUMERO_ATUAL": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "SITUACAO": {"type": DataTypes.STRING(2), "allowNull": True},
    "DATA_LOTE": {"type": DataTypes.TIMESTAMP(), "allowNull": True},
    "NUMERO_INICIAL": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "NUMERO_FINAL": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "OBSERVACAO": {"type": DataTypes.STRING(150), "allowNull": True},
    "SELO_GRUPO_ID": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "SIGLA": {"type": DataTypes.STRING(30), "allowNull": True},
    "NOTA_FISCAL": {"type": DataTypes.STRING(30), "allowNull": True},
    "QUANTIDADE": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "PROTOCOLO_PEDIDO": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "CONFIRMADO": {"type": DataTypes.STRING(2), "allowNull": True},
    "NUMERO_SELO_PRENOTACAO": {"type": DataTypes.STRING(60), "allowNull": True},
    "PROTOCOLO_DO_PEDIDO": {"type": DataTypes.STRING(150), "allowNull": True},
    "TIPO_SELO": {"type": DataTypes.STRING(30), "allowNull": True},
}

G_SELO_LOTE_OPTIONS: dict[str, Any] = {
    "tableName": G_SELO_LOTE_TABLE,
    "primaryKey": "SELO_LOTE_ID",
}


@lru_cache(maxsize=1)
def get_g_selo_lote_model() -> Type[Any]:
    orm = get_orm()

    existing = orm.models.get(G_SELO_LOTE_MODEL_NAME) or orm.models.get(G_SELO_LOTE_TABLE)
    if existing is not None:
        return existing

    return orm.define(
        G_SELO_LOTE_MODEL_NAME,
        G_SELO_LOTE_ATTRIBUTES,
        G_SELO_LOTE_OPTIONS,
    )
