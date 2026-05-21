from __future__ import annotations

from functools import lru_cache
from typing import Any, Type

from orm_py import DataTypes

from database.orm_firebird import get_orm

P_LIVRO_ANDAMENTO_TABLE = "P_LIVRO_ANDAMENTO"
P_LIVRO_ANDAMENTO_MODEL_NAME = "P_LIVRO_ANDAMENTO"

# P_LIVRO_ANDAMENTO — livros de andamento vinculados a P_LIVRO_NATUREZA

P_LIVRO_ANDAMENTO_ATTRIBUTES: dict[str, dict[str, Any]] = {
    "LIVRO_ANDAMENTO_ID": {
        "type": DataTypes.NUMERIC(10, 2),
        "primaryKey": True,
        "autoIncrement": False,
    },
    "LIVRO_NATUREZA_ID": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "FOLHA_ATUAL": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "NUMERO_LIVRO": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "NUMERO_LIVRO_LETRA": {"type": DataTypes.STRING(3), "allowNull": True},
    "DATA_ABERTURA": {"type": DataTypes.TIMESTAMP(), "allowNull": True},
    "DATA_FECHAMENTO": {"type": DataTypes.TIMESTAMP(), "allowNull": True},
    "NUMERO_FOLHAS": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "SIGLA": {"type": DataTypes.STRING(3), "allowNull": True},
    "USUARIO_ID": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
}

P_LIVRO_ANDAMENTO_OPTIONS: dict[str, Any] = {
    "tableName": P_LIVRO_ANDAMENTO_TABLE,
    "primaryKey": "LIVRO_ANDAMENTO_ID",
}


@lru_cache(maxsize=1)
def get_p_livro_andamento_model() -> Type[Any]:
    orm = get_orm()

    existing = orm.models.get(P_LIVRO_ANDAMENTO_MODEL_NAME) or orm.models.get(
        P_LIVRO_ANDAMENTO_TABLE
    )
    if existing is not None:
        return existing

    return orm.define(
        P_LIVRO_ANDAMENTO_MODEL_NAME,
        P_LIVRO_ANDAMENTO_ATTRIBUTES,
        P_LIVRO_ANDAMENTO_OPTIONS,
    )
