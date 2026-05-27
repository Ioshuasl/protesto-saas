from __future__ import annotations

from functools import lru_cache
from typing import Any, Type

from orm_py import DataTypes

from database.orm_firebird import get_orm

G_EMOLUMENTO_TABLE = "G_EMOLUMENTO"
G_EMOLUMENTO_MODEL_NAME = "G_EMOLUMENTO"

G_EMOLUMENTO_ATTRIBUTES: dict[str, dict[str, Any]] = {
    "EMOLUMENTO_ID": {
        "type": DataTypes.NUMERIC(10, 2),
        "primaryKey": True,
        "autoIncrement": False,
        "allowNull": False,
    },
    "DESCRICAO": {"type": DataTypes.STRING(260), "allowNull": True},
    "TIPO": {"type": DataTypes.STRING(1), "allowNull": True},
    "SISTEMA_ID": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "SELO_GRUPO_ID": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "REG_AVERB": {"type": DataTypes.STRING(1), "allowNull": True},
    "PRE_DEFINIDO": {"type": DataTypes.STRING(1), "allowNull": True},
    "SITUACAO": {"type": DataTypes.STRING(1), "allowNull": True},
    "SITUACAO_RI": {"type": DataTypes.STRING(1), "allowNull": True},
    "COM_REDUCAO": {"type": DataTypes.STRING(1), "allowNull": True},
    "MOTIVO_REDUCAO": {"type": DataTypes.STRING(150), "allowNull": True},
    "VALOR_MAXIMO_CERTIDAO": {"type": DataTypes.NUMERIC(14, 3), "allowNull": True},
    "TIPO_OBJETIVO": {"type": DataTypes.STRING(3), "allowNull": True},
    "MODELO_TAG": {"type": DataTypes.STRING(3), "allowNull": True},
    "CODIGO_NOTA_ID": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "CONVENIO_CODHAB": {"type": DataTypes.STRING(1), "allowNull": True},
    "ITEM_DF": {"type": DataTypes.STRING(10), "allowNull": True},
}

G_EMOLUMENTO_OPTIONS: dict[str, Any] = {
    "tableName": G_EMOLUMENTO_TABLE,
    "primaryKey": "EMOLUMENTO_ID",
}


@lru_cache(maxsize=1)
def get_g_emolumento_model() -> Type[Any]:
    orm = get_orm()

    existing = orm.models.get(G_EMOLUMENTO_MODEL_NAME) or orm.models.get(
        G_EMOLUMENTO_TABLE
    )
    if existing is not None:
        return existing

    return orm.define(
        G_EMOLUMENTO_MODEL_NAME,
        G_EMOLUMENTO_ATTRIBUTES,
        G_EMOLUMENTO_OPTIONS,
    )
