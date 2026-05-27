from __future__ import annotations

from functools import lru_cache
from typing import Any, Type

from orm_py import DataTypes

from database.orm_firebird import get_orm

G_EMOLUMENTO_ITEM_TABLE = "G_EMOLUMENTO_ITEM"
G_EMOLUMENTO_ITEM_MODEL_NAME = "G_EMOLUMENTO_ITEM"

G_EMOLUMENTO_ITEM_ATTRIBUTES: dict[str, dict[str, Any]] = {
    "VALOR_EMOLUMENTO": {"type": DataTypes.NUMERIC(14, 3), "allowNull": True},
    "EMOLUMENTO_ITEM_ID": {
        "type": DataTypes.NUMERIC(10, 2),
        "primaryKey": True,
        "autoIncrement": False,
        "allowNull": False,
    },
    "EMOLUMENTO_ID": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "VALOR_INICIO": {"type": DataTypes.NUMERIC(14, 3), "allowNull": True},
    "VALOR_FIM": {"type": DataTypes.NUMERIC(14, 3), "allowNull": True},
    "VALOR_TAXA_JUDICIARIA": {"type": DataTypes.NUMERIC(14, 3), "allowNull": True},
    "EMOLUMENTO_PERIODO_ID": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "CODIGO": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "PAGINA_EXTRA": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "VALOR_PAGINA_EXTRA": {"type": DataTypes.NUMERIC(14, 3), "allowNull": True},
    "VALOR_OUTRA_TAXA1": {"type": DataTypes.NUMERIC(14, 3), "allowNull": True},
    "CODIGO_SELO": {"type": DataTypes.STRING(30), "allowNull": True},
    "VALOR_FUNDO_RI": {"type": DataTypes.NUMERIC(14, 3), "allowNull": True},
    "CODIGO_TABELA": {"type": DataTypes.STRING(30), "allowNull": True},
    "SELO_GRUPO_ID": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "CODIGO_KM": {"type": DataTypes.STRING(30), "allowNull": True},
    "EMOLUMENTO_ACRESCE": {"type": DataTypes.NUMERIC(14, 3), "allowNull": True},
    "TAXA_ACRESCE": {"type": DataTypes.NUMERIC(14, 3), "allowNull": True},
    "FUNCIVIL_ACRESCE": {"type": DataTypes.NUMERIC(14, 3), "allowNull": True},
    "VALOR_FRACAO": {"type": DataTypes.NUMERIC(14, 3), "allowNull": True},
    "VALOR_POR_EXCEDENTE_EMOL": {"type": DataTypes.NUMERIC(14, 3), "allowNull": True},
    "VALOR_POR_EXCEDENTE_TJ": {"type": DataTypes.NUMERIC(14, 3), "allowNull": True},
    "VALOR_POR_EXCEDENTE_FUNDO": {"type": DataTypes.NUMERIC(14, 3), "allowNull": True},
    "VALOR_LIMITE_EXCEDENTE_EMOL": {"type": DataTypes.NUMERIC(14, 3), "allowNull": True},
    "VALOR_LIMITE_EXCEDENTE_TJ": {"type": DataTypes.NUMERIC(14, 3), "allowNull": True},
    "VALOR_LIMITE_EXCEDENTE_FUNDO": {"type": DataTypes.NUMERIC(14, 3), "allowNull": True},
    "FUNDO_SELO": {"type": DataTypes.NUMERIC(14, 3), "allowNull": True},
    "DISTRIBUICAO": {"type": DataTypes.NUMERIC(14, 3), "allowNull": True},
    "VRCEXT": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
}

G_EMOLUMENTO_ITEM_OPTIONS: dict[str, Any] = {
    "tableName": G_EMOLUMENTO_ITEM_TABLE,
    "primaryKey": "EMOLUMENTO_ITEM_ID",
}


@lru_cache(maxsize=1)
def get_g_emolumento_item_model() -> Type[Any]:
    orm = get_orm()

    existing = orm.models.get(G_EMOLUMENTO_ITEM_MODEL_NAME) or orm.models.get(
        G_EMOLUMENTO_ITEM_TABLE
    )
    if existing is not None:
        return existing

    return orm.define(
        G_EMOLUMENTO_ITEM_MODEL_NAME,
        G_EMOLUMENTO_ITEM_ATTRIBUTES,
        G_EMOLUMENTO_ITEM_OPTIONS,
    )
