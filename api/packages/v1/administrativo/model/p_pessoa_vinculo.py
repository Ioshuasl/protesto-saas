from __future__ import annotations

from functools import lru_cache
from typing import Any, Type

from orm_py import DataTypes

from database.orm_firebird import get_orm

P_PESSOA_VINCULO_TABLE = "P_PESSOA_VINCULO"
P_PESSOA_VINCULO_MODEL_NAME = "P_PESSOA_VINCULO"

# P_PESSOA_VINCULO — vínculos de pessoa com título (devedor, credor, apresentante, etc.)
# Gerado a partir de QueryInterface.describe_table (Firebird santarita).
# VARCHAR(1): PRINCIPAL, FAVORECIDO, GERAR_SELO, DEVEDOR_TIPO_ACEITE, DEVEDOR_MICROEMPRESA → STRING(2)

P_PESSOA_VINCULO_ATTRIBUTES: dict[str, dict[str, Any]] = {
    "PESSOA_VINCULO_ID": {
        "type": DataTypes.NUMERIC(10, 0),
        "primaryKey": True,
        "autoIncrement": False,
        "allowNull": False,
    },
    "NOME": {"type": DataTypes.STRING(150), "allowNull": True},
    "CPFCNPJ": {"type": DataTypes.STRING(15), "allowNull": True},
    "ENDERECO": {"type": DataTypes.STRING(90), "allowNull": True},
    "BAIRRO": {"type": DataTypes.STRING(60), "allowNull": True},
    "CIDADE": {"type": DataTypes.STRING(60), "allowNull": True},
    "UF": {"type": DataTypes.STRING(3), "allowNull": True},
    "CEP": {"type": DataTypes.STRING(15), "allowNull": True},
    "TELEFONE": {"type": DataTypes.STRING(15), "allowNull": True},
    "RG": {"type": DataTypes.STRING(30), "allowNull": True},
    "TITULO_ID": {"type": DataTypes.NUMERIC(10, 0), "allowNull": True},
    "TIPO_VINCULO": {"type": DataTypes.STRING(15), "allowNull": True},
    "PESSOA_ID": {"type": DataTypes.NUMERIC(10, 0), "allowNull": True},
    "BANCO": {"type": DataTypes.STRING(3), "allowNull": True},
    "AGENCIA": {"type": DataTypes.STRING(30), "allowNull": True},
    "CONTA": {"type": DataTypes.STRING(30), "allowNull": True},
    "NOME_BANCO": {"type": DataTypes.STRING(30), "allowNull": True},
    "NACIONALIDADE": {"type": DataTypes.STRING(30), "allowNull": True},
    "ESTADO_CIVIL_ID": {"type": DataTypes.NUMERIC(10, 0), "allowNull": True},
    "PROFISSAO_ID": {"type": DataTypes.NUMERIC(10, 0), "allowNull": True},
    "CIDADE_AGENCIA": {"type": DataTypes.STRING(30), "allowNull": True},
    "PRINCIPAL": {"type": DataTypes.STRING(2), "allowNull": True},
    "FAVORECIDO": {"type": DataTypes.STRING(2), "allowNull": True},
    "GERAR_SELO": {"type": DataTypes.STRING(2), "allowNull": True},
    "DEVEDOR_DATA_ACEITE": {"type": DataTypes.TIMESTAMP(), "allowNull": True},
    "DEVEDOR_AGENCIA": {"type": DataTypes.STRING(90), "allowNull": True},
    "DEVEDOR_NUMERO_AR": {"type": DataTypes.STRING(90), "allowNull": True},
    "DEVEDOR_RECEBIDO_POR": {"type": DataTypes.STRING(90), "allowNull": True},
    "DEVEDOR_SITUACAO": {"type": DataTypes.STRING(90), "allowNull": True},
    "DEVEDOR_TIPO_ACEITE": {"type": DataTypes.STRING(2), "allowNull": True},
    "OCORRENCIA_ID": {"type": DataTypes.NUMERIC(10, 0), "allowNull": True},
    "CHAVE_IMPORTACAO": {"type": DataTypes.NUMERIC(10, 0), "allowNull": True},
    "DEVEDOR_MICROEMPRESA": {"type": DataTypes.STRING(2), "allowNull": True},
    "OCORRENCIA_ANDAMENTO_ID": {"type": DataTypes.NUMERIC(10, 0), "allowNull": True},
    "CONTROLE_DEVEDOR": {"type": DataTypes.NUMERIC(10, 0), "allowNull": True},
}

P_PESSOA_VINCULO_OPTIONS: dict[str, Any] = {
    "tableName": P_PESSOA_VINCULO_TABLE,
    "primaryKey": "PESSOA_VINCULO_ID",
}


@lru_cache(maxsize=1)
def get_p_pessoa_vinculo_model() -> Type[Any]:
    orm = get_orm()

    existing = orm.models.get(P_PESSOA_VINCULO_MODEL_NAME) or orm.models.get(
        P_PESSOA_VINCULO_TABLE
    )
    if existing is not None:
        return existing

    return orm.define(
        P_PESSOA_VINCULO_MODEL_NAME,
        P_PESSOA_VINCULO_ATTRIBUTES,
        P_PESSOA_VINCULO_OPTIONS,
    )
