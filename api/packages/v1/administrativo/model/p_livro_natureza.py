from __future__ import annotations

from functools import lru_cache
from typing import Any, Type

from orm_py import DataTypes

from database.orm_firebird import get_orm

P_LIVRO_NATUREZA_TABLE = "P_LIVRO_NATUREZA"
P_LIVRO_NATUREZA_MODEL_NAME = "P_LIVRO_NATUREZA"

# P_LIVRO_NATUREZA — naturezas de livro (protesto)
# SITUACAO: A = Ativo, I ou null = Inativo (API normaliza para exibição)

P_LIVRO_NATUREZA_ATTRIBUTES: dict[str, dict[str, Any]] = {
    "LIVRO_NATUREZA_ID": {
        "type": DataTypes.NUMERIC(10, 2),
        "primaryKey": True,
        "autoIncrement": False,
    },
    "NATUREZA_ID": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "DESCRICAO": {"type": DataTypes.STRING(60), "allowNull": True},
    "SITUACAO": {"type": DataTypes.STRING(1), "allowNull": True},
    "SIGLA": {"type": DataTypes.STRING(3), "allowNull": True},
    "TIPO": {"type": DataTypes.STRING(1), "allowNull": True},
}

P_LIVRO_NATUREZA_OPTIONS: dict[str, Any] = {
    "tableName": P_LIVRO_NATUREZA_TABLE,
    "primaryKey": "LIVRO_NATUREZA_ID",
}


@lru_cache(maxsize=1)
def get_p_livro_natureza_model() -> Type[Any]:
    orm = get_orm()

    existing = orm.models.get(P_LIVRO_NATUREZA_MODEL_NAME) or orm.models.get(
        P_LIVRO_NATUREZA_TABLE
    )
    if existing is not None:
        return existing

    return orm.define(
        P_LIVRO_NATUREZA_MODEL_NAME,
        P_LIVRO_NATUREZA_ATTRIBUTES,
        P_LIVRO_NATUREZA_OPTIONS,
    )
