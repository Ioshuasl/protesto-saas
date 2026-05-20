from __future__ import annotations

from functools import lru_cache
from typing import Any, Type

from orm_py import DataTypes

from database.orm_firebird import get_orm

G_FERIADO_TABLE = "G_FERIADO"
G_FERIADO_MODEL_NAME = "G_FERIADO"

# Domínio Firebird (VARCHAR(1)); API expõe apenas siglas (g_feriado_schema.py):
#   TIPO — F = fixo, V = variável
#   SITUACAO — A = ativo; I, vazio ou NULL no banco → I na resposta

G_FERIADO_ATTRIBUTES: dict[str, dict[str, Any]] = {
    "FERIADO_ID": {
        "type": DataTypes.NUMERIC(10, 0),
        "primaryKey": True,
        "autoIncrement": False,
    },
    "ANO": {"type": DataTypes.INTEGER(), "allowNull": True},
    "MES": {"type": DataTypes.INTEGER(), "allowNull": True},
    "DIA": {"type": DataTypes.INTEGER(), "allowNull": True},
    "DATA": {"type": DataTypes.TIMESTAMP(), "allowNull": False},
    "DESCRICAO": {"type": DataTypes.STRING(60), "allowNull": True},
    "TIPO": {"type": DataTypes.STRING(2), "allowNull": True},
    "SITUACAO": {"type": DataTypes.STRING(2), "allowNull": True},
}

G_FERIADO_OPTIONS: dict[str, Any] = {
    "tableName": G_FERIADO_TABLE,
    "primaryKey": "FERIADO_ID",
}


@lru_cache(maxsize=1)
def get_g_feriado_model() -> Type[Any]:
    orm = get_orm()

    existing = orm.models.get(G_FERIADO_MODEL_NAME) or orm.models.get(G_FERIADO_TABLE)
    if existing is not None:
        return existing

    return orm.define(
        G_FERIADO_MODEL_NAME,
        G_FERIADO_ATTRIBUTES,
        G_FERIADO_OPTIONS,
    )
