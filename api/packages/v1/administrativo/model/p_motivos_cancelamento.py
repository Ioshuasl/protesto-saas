from __future__ import annotations

from functools import lru_cache
from typing import Any, Type

from orm_py import DataTypes

from database.orm_firebird import get_orm

P_MOTIVOS_CANCELAMENTO_TABLE = "P_MOTIVOS_CANCELAMENTO"
P_MOTIVOS_CANCELAMENTO_MODEL_NAME = "P_MOTIVOS_CANCELAMENTO"

# Domínio Firebird (describe_table + amostra 2026-05-22):
#   MOTIVOS_CANCELAMENTO_ID — NUMERIC(10,2) na DDL legada; valores inteiros 1..n
#   DESCRICAO               — VARCHAR(60)
#   SITUACAO                — VARCHAR(15): A = ativo; NULL/vazio → I na resposta API
#   ORD_JUD_OU_REM_IND      — VARCHAR(1); siglas API a confirmar (amostra: NULL)
# FK: P_TITULO.MOTIVO_CANCELAMENTO → P_MOTIVOS_CANCELAMENTO.MOTIVOS_CANCELAMENTO_ID

P_MOTIVOS_CANCELAMENTO_ATTRIBUTES: dict[str, dict[str, Any]] = {
    "MOTIVOS_CANCELAMENTO_ID": {
        "type": DataTypes.NUMERIC(10, 0),
        "primaryKey": True,
        "autoIncrement": False,
    },
    "DESCRICAO": {"type": DataTypes.STRING(60), "allowNull": True},
    "SITUACAO": {"type": DataTypes.STRING(15), "allowNull": True},
    "ORD_JUD_OU_REM_IND": {"type": DataTypes.STRING(1), "allowNull": True},
}

P_MOTIVOS_CANCELAMENTO_OPTIONS: dict[str, Any] = {
    "tableName": P_MOTIVOS_CANCELAMENTO_TABLE,
    "primaryKey": "MOTIVOS_CANCELAMENTO_ID",
}


@lru_cache(maxsize=1)
def get_p_motivos_cancelamento_model() -> Type[Any]:
    orm = get_orm()

    existing = orm.models.get(P_MOTIVOS_CANCELAMENTO_MODEL_NAME) or orm.models.get(
        P_MOTIVOS_CANCELAMENTO_TABLE
    )
    if existing is not None:
        return existing

    return orm.define(
        P_MOTIVOS_CANCELAMENTO_MODEL_NAME,
        P_MOTIVOS_CANCELAMENTO_ATTRIBUTES,
        P_MOTIVOS_CANCELAMENTO_OPTIONS,
    )
