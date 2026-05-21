from __future__ import annotations

from functools import lru_cache
from typing import Any, Type

from orm_py import DataTypes

from database.orm_firebird import get_orm

G_TB_PROFISSAO_TABLE = "G_TB_PROFISSAO"
G_TB_PROFISSAO_MODEL_NAME = "G_TB_PROFISSAO"

# G_TB_PROFISSAO — tabela de domínio profissão
# Gerado a partir de QueryInterface.describe_table (Firebird santarita).

G_TB_PROFISSAO_ATTRIBUTES: dict[str, dict[str, Any]] = {
    "TB_PROFISSAO_ID": {"type": DataTypes.NUMERIC(10, 0), "primaryKey": True, "autoIncrement": False, "allowNull": False},
    "DESCRICAO": {"type": DataTypes.STRING(60), "allowNull": True},
    "SITUACAO": {"type": DataTypes.STRING(2), "allowNull": True},
    "COD_CBO": {"type": DataTypes.STRING(10), "allowNull": True},
}

G_TB_PROFISSAO_OPTIONS: dict[str, Any] = {
    "tableName": G_TB_PROFISSAO_TABLE,
    "primaryKey": "TB_PROFISSAO_ID",
}


@lru_cache(maxsize=1)
def get_g_tb_profissao_model() -> Type[Any]:
    orm = get_orm()

    existing = orm.models.get(G_TB_PROFISSAO_MODEL_NAME) or orm.models.get(G_TB_PROFISSAO_TABLE)
    if existing is not None:
        return existing

    return orm.define(
        G_TB_PROFISSAO_MODEL_NAME,
        G_TB_PROFISSAO_ATTRIBUTES,
        G_TB_PROFISSAO_OPTIONS,
    )
