from __future__ import annotations

from functools import lru_cache
from typing import Any, Type

from orm_py import DataTypes

from database.orm_firebird import get_orm

G_TB_ESTADOCIVIL_TABLE = "G_TB_ESTADOCIVIL"
G_TB_ESTADOCIVIL_MODEL_NAME = "G_TB_ESTADOCIVIL"

# G_TB_ESTADOCIVIL — tabela de domínio estado civil
# Gerado a partir de QueryInterface.describe_table (Firebird santarita).

G_TB_ESTADOCIVIL_ATTRIBUTES: dict[str, dict[str, Any]] = {
    "TB_ESTADOCIVIL_ID": {"type": DataTypes.NUMERIC(10, 0), "primaryKey": True, "autoIncrement": False, "allowNull": False},
    "DESCRICAO": {"type": DataTypes.STRING(60), "allowNull": True},
    "SITUACAO": {"type": DataTypes.STRING(2), "allowNull": True},
    "SISTEMA_ID": {"type": DataTypes.NUMERIC(10, 0), "allowNull": True},
    "TIPO": {"type": DataTypes.NUMERIC(10, 0), "allowNull": True},
}

G_TB_ESTADOCIVIL_OPTIONS: dict[str, Any] = {
    "tableName": G_TB_ESTADOCIVIL_TABLE,
    "primaryKey": "TB_ESTADOCIVIL_ID",
}


@lru_cache(maxsize=1)
def get_g_tb_estadocivil_model() -> Type[Any]:
    orm = get_orm()

    existing = orm.models.get(G_TB_ESTADOCIVIL_MODEL_NAME) or orm.models.get(G_TB_ESTADOCIVIL_TABLE)
    if existing is not None:
        return existing

    return orm.define(
        G_TB_ESTADOCIVIL_MODEL_NAME,
        G_TB_ESTADOCIVIL_ATTRIBUTES,
        G_TB_ESTADOCIVIL_OPTIONS,
    )
