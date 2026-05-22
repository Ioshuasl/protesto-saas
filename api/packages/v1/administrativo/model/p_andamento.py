from __future__ import annotations

from functools import lru_cache
from typing import Any, Type

from orm_py import DataTypes

from database.orm_firebird import get_orm

P_ANDAMENTO_TABLE = "P_ANDAMENTO"
P_ANDAMENTO_MODEL_NAME = "P_ANDAMENTO"

# P_ANDAMENTO — histórico de andamento do título (protesto)
# Introspecção describe_table (Firebird):
#   ANDAMENTO_ID              — NUMERIC(10,2) PK
#   OCORRENCIA_ANDAMENTO_ID   — NUMERIC(10,2) FK → P_OCORRENCIA_ANDAMENTO
#   TITULO_ID                 — NUMERIC(10,2) FK → P_TITULO
#   USUARIO_ID                — NUMERIC(10,2) FK → G_USUARIO
#   ARQUIVO_GERADO            — VARCHAR(1); API: D = Aguardando, E = Exportado
#   DATA_OCORRENCIA, DATA_GERACAO — TIMESTAMP

P_ANDAMENTO_ATTRIBUTES: dict[str, dict[str, Any]] = {
    "ANDAMENTO_ID": {
        "type": DataTypes.NUMERIC(10, 2),
        "primaryKey": True,
        "autoIncrement": False,
        "allowNull": False,
    },
    "OCORRENCIA_ANDAMENTO_ID": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "DATA_OCORRENCIA": {"type": DataTypes.TIMESTAMP(), "allowNull": True},
    "TITULO_ID": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "USUARIO_ID": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "ARQUIVO_GERADO": {"type": DataTypes.STRING(2), "allowNull": True},
    "DATA_GERACAO": {"type": DataTypes.TIMESTAMP(), "allowNull": True},
}

P_ANDAMENTO_OPTIONS: dict[str, Any] = {
    "tableName": P_ANDAMENTO_TABLE,
    "primaryKey": "ANDAMENTO_ID",
}


@lru_cache(maxsize=1)
def get_p_andamento_model() -> Type[Any]:
    orm = get_orm()

    existing = orm.models.get(P_ANDAMENTO_MODEL_NAME) or orm.models.get(P_ANDAMENTO_TABLE)
    if existing is not None:
        return existing

    return orm.define(
        P_ANDAMENTO_MODEL_NAME,
        P_ANDAMENTO_ATTRIBUTES,
        P_ANDAMENTO_OPTIONS,
    )
