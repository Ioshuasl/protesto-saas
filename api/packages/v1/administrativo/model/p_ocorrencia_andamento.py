from __future__ import annotations

from functools import lru_cache
from typing import Any, Type

from orm_py import DataTypes

from database.orm_firebird import get_orm

P_OCORRENCIA_ANDAMENTO_TABLE = "P_OCORRENCIA_ANDAMENTO"
P_OCORRENCIA_ANDAMENTO_MODEL_NAME = "P_OCORRENCIA_ANDAMENTO"

# P_OCORRENCIA_ANDAMENTO — cadastro de ocorrências de andamento (protesto)
# Introspecção describe_table (Firebird):
#   OCORRENCIA_ANDAMENTO_ID — NUMERIC(10,2) PK (valores inteiros 1..n na amostra)
#   CODIGO                  — VARCHAR(10), siglas (ex.: AA..AK)
#   DESCRICAO               — VARCHAR(260)
# FK: P_TITULO.OCORRENCIA_ANDAMENTO_ID, P_ANDAMENTO.OCORRENCIA_ANDAMENTO_ID

P_OCORRENCIA_ANDAMENTO_ATTRIBUTES: dict[str, dict[str, Any]] = {
    "OCORRENCIA_ANDAMENTO_ID": {
        "type": DataTypes.NUMERIC(10, 2),
        "primaryKey": True,
        "autoIncrement": False,
        "allowNull": False,
    },
    "CODIGO": {"type": DataTypes.STRING(10), "allowNull": True},
    "DESCRICAO": {"type": DataTypes.STRING(260), "allowNull": True},
}

P_OCORRENCIA_ANDAMENTO_OPTIONS: dict[str, Any] = {
    "tableName": P_OCORRENCIA_ANDAMENTO_TABLE,
    "primaryKey": "OCORRENCIA_ANDAMENTO_ID",
}


@lru_cache(maxsize=1)
def get_p_ocorrencia_andamento_model() -> Type[Any]:
    orm = get_orm()

    existing = orm.models.get(P_OCORRENCIA_ANDAMENTO_MODEL_NAME) or orm.models.get(
        P_OCORRENCIA_ANDAMENTO_TABLE
    )
    if existing is not None:
        return existing

    return orm.define(
        P_OCORRENCIA_ANDAMENTO_MODEL_NAME,
        P_OCORRENCIA_ANDAMENTO_ATTRIBUTES,
        P_OCORRENCIA_ANDAMENTO_OPTIONS,
    )
