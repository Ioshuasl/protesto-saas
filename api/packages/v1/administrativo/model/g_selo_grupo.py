from __future__ import annotations

from functools import lru_cache
from typing import Any, Type

from orm_py import DataTypes

from database.orm_firebird import get_orm

G_SELO_GRUPO_TABLE = "G_SELO_GRUPO"
G_SELO_GRUPO_MODEL_NAME = "G_SELO_GRUPO"

# G_SELO_GRUPO — grupos de selos
# DDL Firebird: NUMERICO = NUMERIC(10,2); DINHEIRO = NUMERIC(14,3); VARCHAR_001 = VARCHAR(1)

G_SELO_GRUPO_ATTRIBUTES: dict[str, dict[str, Any]] = {
    "SELO_GRUPO_ID": {
        "type": DataTypes.NUMERIC(10, 2),
        "primaryKey": True,
        "autoIncrement": False,
        "allowNull": False,
    },
    "DESCRICAO": {"type": DataTypes.STRING(260), "allowNull": True},
    "NUMERO": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "SITUACAO": {"type": DataTypes.STRING(1), "allowNull": True},
    "CONTROLE_AUTOMATICO": {"type": DataTypes.STRING(1), "allowNull": True},
    "SISTEMA_ID": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "VALOR": {"type": DataTypes.NUMERIC(14, 3), "allowNull": True},
    "TIPO_CARTORIO": {"type": DataTypes.STRING(3), "allowNull": True},
    "DESCRICAO_COMPLETA": {"type": DataTypes.STRING(260), "allowNull": True},
    "AGRUPADOR": {"type": DataTypes.STRING(1), "allowNull": True},
    "UM_POR_PROTOCOLO": {"type": DataTypes.STRING(1), "allowNull": True},
    "NUMERO_PRINCIPAL_INI": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "NUMERO_PRINCIPAL_FIM": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "SELO_GRUPO_ID_PRINCIPAL": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "ENVIO_AUTOMATICO": {"type": DataTypes.STRING(1), "allowNull": True},
    "SELO_GRUPO_ID_AGRUPADOR": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "CODIGO_CONTA": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "ID_TIPO_ATO_ANTIGO": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "GRUPOS_PRINCIPAL": {"type": DataTypes.STRING(260), "allowNull": True},
    "SIGLA": {"type": DataTypes.STRING(10), "allowNull": True},
    "TIPO_SELO": {"type": DataTypes.STRING(10), "allowNull": True},
    "NATUREZA": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
}

G_SELO_GRUPO_OPTIONS: dict[str, Any] = {
    "tableName": G_SELO_GRUPO_TABLE,
    "primaryKey": "SELO_GRUPO_ID",
}


@lru_cache(maxsize=1)
def get_g_selo_grupo_model() -> Type[Any]:
    orm = get_orm()

    existing = orm.models.get(G_SELO_GRUPO_MODEL_NAME) or orm.models.get(G_SELO_GRUPO_TABLE)
    if existing is not None:
        return existing

    return orm.define(
        G_SELO_GRUPO_MODEL_NAME,
        G_SELO_GRUPO_ATTRIBUTES,
        G_SELO_GRUPO_OPTIONS,
    )
