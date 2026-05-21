from __future__ import annotations

from functools import lru_cache
from typing import Any, Type

from orm_py import DataTypes

from database.orm_firebird import get_orm

P_PESSOA_TABLE = "P_PESSOA"
P_PESSOA_MODEL_NAME = "P_PESSOA"

# P_PESSOA — cadastro de pessoas (protesto)
# Gerado a partir de QueryInterface.describe_table (Firebird santarita).

P_PESSOA_ATTRIBUTES: dict[str, dict[str, Any]] = {
    "PESSOA_ID": {"type": DataTypes.NUMERIC(10, 0), "primaryKey": True, "autoIncrement": False, "allowNull": False},
    "NOME": {"type": DataTypes.STRING(150), "allowNull": True},
    "CPFCNPJ": {"type": DataTypes.STRING(15), "allowNull": True},
    "ENDERECO": {"type": DataTypes.STRING(90), "allowNull": True},
    "BAIRRO": {"type": DataTypes.STRING(60), "allowNull": True},
    "CIDADE": {"type": DataTypes.STRING(60), "allowNull": True},
    "UF": {"type": DataTypes.STRING(3), "allowNull": True},
    "CEP": {"type": DataTypes.STRING(15), "allowNull": True},
    "TELEFONE": {"type": DataTypes.STRING(15), "allowNull": True},
    "RG": {"type": DataTypes.STRING(30), "allowNull": True},
    "OBSERVACOES": {"type": DataTypes.STRING(260), "allowNull": True},
    "BANCO": {"type": DataTypes.STRING(3), "allowNull": True},
    "AGENCIA": {"type": DataTypes.STRING(30), "allowNull": True},
    "CONTA": {"type": DataTypes.STRING(30), "allowNull": True},
    "NOME_BANCO": {"type": DataTypes.STRING(30), "allowNull": True},
    "NACIONALIDADE": {"type": DataTypes.STRING(30), "allowNull": True},
    "ESTADO_CIVIL_ID": {"type": DataTypes.NUMERIC(10, 0), "allowNull": True},
    "PROFISSAO_ID": {"type": DataTypes.NUMERIC(10, 0), "allowNull": True},
    "CIDADE_AGENCIA": {"type": DataTypes.STRING(30), "allowNull": True},
    "DATA_NASCIMENTO": {"type": DataTypes.TIMESTAMP(), "allowNull": True},
    "EMAIL": {"type": DataTypes.STRING(60), "allowNull": True},
    "CIDADE_ID": {"type": DataTypes.NUMERIC(10, 0), "allowNull": True},
    "DATA_VALIDADE": {"type": DataTypes.TIMESTAMP(), "allowNull": True},
    "MICRO_EMPRESA": {"type": DataTypes.STRING(2), "allowNull": True},
    "CHAVE_PESSOA_IMP": {"type": DataTypes.NUMERIC(10, 0), "allowNull": True},
    "COD_CRA": {"type": DataTypes.STRING(30), "allowNull": True},
    "NOME_FANTASIA": {"type": DataTypes.STRING(260), "allowNull": True},
}

P_PESSOA_OPTIONS: dict[str, Any] = {
    "tableName": P_PESSOA_TABLE,
    "primaryKey": "PESSOA_ID",
}


@lru_cache(maxsize=1)
def get_p_pessoa_model() -> Type[Any]:
    orm = get_orm()

    existing = orm.models.get(P_PESSOA_MODEL_NAME) or orm.models.get(P_PESSOA_TABLE)
    if existing is not None:
        return existing

    return orm.define(
        P_PESSOA_MODEL_NAME,
        P_PESSOA_ATTRIBUTES,
        P_PESSOA_OPTIONS,
    )
