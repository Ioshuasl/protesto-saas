from __future__ import annotations

from functools import lru_cache
from typing import Any, Type

from orm_py import DataTypes

from database.orm_firebird import get_orm

P_MOTIVOS_TABLE = "P_MOTIVOS"
P_MOTIVOS_MODEL_NAME = "P_MOTIVOS"

# Domínio Firebird (introspecção describe_table + amostra):
#   MOTIVOS_ID — NUMERIC(8), PK (valores inteiros 1..n)
#   DESCRICAO  — VARCHAR(60)
#   SITUACAO   — VARCHAR(15): A = ativo; NULL/vazio → I na resposta API
#   CODIGO     — VARCHAR(3), códigos numéricos como string ("1", "2", …)
# FK: P_TITULO.MOTIVO_APONTAMENTO_ID → P_MOTIVOS.MOTIVOS_ID

P_MOTIVOS_ATTRIBUTES: dict[str, dict[str, Any]] = {
    "MOTIVOS_ID": {
        "type": DataTypes.NUMERIC(10, 0),
        "primaryKey": True,
        "autoIncrement": False,
    },
    "DESCRICAO": {"type": DataTypes.STRING(60), "allowNull": True},
    "SITUACAO": {"type": DataTypes.STRING(15), "allowNull": True},
    "CODIGO": {"type": DataTypes.STRING(3), "allowNull": True},
}

P_MOTIVOS_OPTIONS: dict[str, Any] = {
    "tableName": P_MOTIVOS_TABLE,
    "primaryKey": "MOTIVOS_ID",
}


@lru_cache(maxsize=1)
def get_p_motivos_model() -> Type[Any]:
    orm = get_orm()

    existing = orm.models.get(P_MOTIVOS_MODEL_NAME) or orm.models.get(P_MOTIVOS_TABLE)
    if existing is not None:
        return existing

    return orm.define(
        P_MOTIVOS_MODEL_NAME,
        P_MOTIVOS_ATTRIBUTES,
        P_MOTIVOS_OPTIONS,
    )
