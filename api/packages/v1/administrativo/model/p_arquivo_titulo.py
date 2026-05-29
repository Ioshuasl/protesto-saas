from __future__ import annotations

from functools import lru_cache
from typing import Any, Type

from orm_py import DataTypes

from database.orm_firebird import get_orm

P_ARQUIVO_TITULO_TABLE = "P_ARQUIVO_TITULO"
P_ARQUIVO_TITULO_MODEL_NAME = "P_ARQUIVO_TITULO"

# P_ARQUIVO_TITULO — arquivos de remessa CRA (importação de títulos)
# Domínios Firebird: NUMERICO = NUMERIC(10,2); DATAHORA = TIMESTAMP;
# TEXTO_BLOB = BLOB SUB_TYPE BINARY SEGMENT SIZE 80

P_ARQUIVO_TITULO_ATTRIBUTES: dict[str, dict[str, Any]] = {
    "ARQUIVO_TITULO_ID": {
        "type": DataTypes.NUMERIC(10, 2),
        "primaryKey": True,
        "autoIncrement": False,
        "allowNull": False,
    },
    "DATA_IMPORTACAO": {"type": DataTypes.TIMESTAMP(), "allowNull": True},
    "QUANTIDADE": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "DATA_MOVIMENTO": {"type": DataTypes.STRING(30), "allowNull": True},
    "NUMERO_SEQUENCIAL": {"type": DataTypes.STRING(30), "allowNull": True},
    "QTDE_REGISTROS": {"type": DataTypes.STRING(30), "allowNull": True},
    "QTDE_TITULOS": {"type": DataTypes.STRING(30), "allowNull": True},
    "QTDE_INDICACOES": {"type": DataTypes.STRING(30), "allowNull": True},
    "QTDE_ORIGINAIS": {"type": DataTypes.STRING(30), "allowNull": True},
    "SOMA_VLR_REMESSA": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "SOMA_QTDE_REMESSA": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "AGENCIA_CENTRALIZADORA": {"type": DataTypes.STRING(10), "allowNull": True},
    "CODIGO_PRACA": {"type": DataTypes.STRING(10), "allowNull": True},
    "SEQUENCIAL_HEADER": {"type": DataTypes.STRING(10), "allowNull": True},
    "NOME_ARQUIVO": {"type": DataTypes.STRING(150), "allowNull": True},
    "PORTADOR_NOME": {"type": DataTypes.STRING(60), "allowNull": True},
    "COMPLEMENTO_HEADER": {"type": DataTypes.STRING(260), "allowNull": True},
    "IDENTIFICACAO_REGISTRO": {"type": DataTypes.STRING(1), "allowNull": True},
    "PORTADOR_CODIGO": {"type": DataTypes.STRING(3), "allowNull": True},
    "ID_TRANSACAO_REMETENTE": {"type": DataTypes.STRING(3), "allowNull": True},
    "ID_TRANSACAO_DESTINATARIO": {"type": DataTypes.STRING(3), "allowNull": True},
    "ID_TRANSACAO_TIPO": {"type": DataTypes.STRING(3), "allowNull": True},
    "VERSAO_LAYOUT": {"type": DataTypes.STRING(3), "allowNull": True},
    "SEQUENCIAL_FOOTER": {"type": DataTypes.STRING(15), "allowNull": True},
    "COMPLEMENTO_REGISTRO": {"type": DataTypes.STRING(1000), "allowNull": True},
    "TEXTO": {"type": DataTypes.BLOB_BINARY(), "allowNull": True},
    "TEXTO_IMPORTADO": {"type": DataTypes.BLOB_BINARY(), "allowNull": True},
}

P_ARQUIVO_TITULO_OPTIONS: dict[str, Any] = {
    "tableName": P_ARQUIVO_TITULO_TABLE,
    "primaryKey": "ARQUIVO_TITULO_ID",
}


@lru_cache(maxsize=1)
def get_p_arquivo_titulo_model() -> Type[Any]:
    orm = get_orm()

    existing = orm.models.get(P_ARQUIVO_TITULO_MODEL_NAME) or orm.models.get(
        P_ARQUIVO_TITULO_TABLE
    )
    if existing is not None:
        return existing

    return orm.define(
        P_ARQUIVO_TITULO_MODEL_NAME,
        P_ARQUIVO_TITULO_ATTRIBUTES,
        P_ARQUIVO_TITULO_OPTIONS,
    )
