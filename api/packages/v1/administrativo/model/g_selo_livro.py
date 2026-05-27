from __future__ import annotations

from functools import lru_cache
from typing import Any, Type

from orm_py import DataTypes

from database.orm_firebird import get_orm

G_SELO_LIVRO_TABLE = "G_SELO_LIVRO"
G_SELO_LIVRO_MODEL_NAME = "G_SELO_LIVRO"

# G_SELO_LIVRO — registros de selos no livro
# FKs: SELO_LOTE_ID → G_SELO_LOTE; USUARIO_ID / USUARIO_ID_EXPORTACAO → G_USUARIO
# DINHEIRO = NUMERIC(14,3); TEXTO_BLOB = BLOB SUB_TYPE BINARY

G_SELO_LIVRO_ATTRIBUTES: dict[str, dict[str, Any]] = {
    "SELO_LIVRO_ID": {
        "type": DataTypes.NUMERIC(10, 2),
        "primaryKey": True,
        "autoIncrement": False,
        "allowNull": False,
    },
    "NUMERO": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "SELO_SITUACAO_ID": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "OBSERVACAO": {"type": DataTypes.STRING(90), "allowNull": True},
    "SELO_LOTE_ID": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "SIGLA": {"type": DataTypes.STRING(30), "allowNull": True},
    "DESCRICAO": {"type": DataTypes.STRING(260), "allowNull": True},
    "TABELA": {"type": DataTypes.STRING(30), "allowNull": True},
    "CAMPO_ID": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "USUARIO_ID": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "INFORMADO": {"type": DataTypes.STRING(1), "allowNull": True},
    "DATA_INFORMACAO": {"type": DataTypes.TIMESTAMP(), "allowNull": True},
    "RESERVADO": {"type": DataTypes.STRING(1), "allowNull": True},
    "NUMERO_AGRUPADOR": {"type": DataTypes.STRING(30), "allowNull": True},
    "APRESENTANTE": {"type": DataTypes.STRING(150), "allowNull": True},
    "IP_MAQUINA": {"type": DataTypes.STRING(30), "allowNull": True},
    "VALOR_TOTAL": {"type": DataTypes.NUMERIC(14, 3), "allowNull": True},
    "VALOR_EMOLUMENTO": {"type": DataTypes.NUMERIC(14, 3), "allowNull": True},
    "VALOR_TAXA_JUDICIARIA": {"type": DataTypes.NUMERIC(14, 3), "allowNull": True},
    "VALOR_FUNDESP": {"type": DataTypes.NUMERIC(14, 3), "allowNull": True},
    "DATA_EXPORTACAO": {"type": DataTypes.TIMESTAMP(), "allowNull": True},
    "CODIGO_EXPORTACAO": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "DATA": {"type": DataTypes.TIMESTAMP(), "allowNull": True},
    "USUARIO_ID_EXPORTACAO": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "SELO_CONSOLIDACAO_ID": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "STATUS_CONSOLIDACAO": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "DATA_RECEBIMENTO_TJ": {"type": DataTypes.TIMESTAMP(), "allowNull": True},
    "TAG_SELO": {"type": DataTypes.BLOB_BINARY(), "allowNull": True},
    "VALOR_ISS": {"type": DataTypes.NUMERIC(14, 3), "allowNull": True},
    "VALIDACAO": {"type": DataTypes.STRING(60), "allowNull": True},
    "ID_DO_ATO_ISENTADO": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "MOTIVO_ISENCAO": {"type": DataTypes.STRING(260), "allowNull": True},
    "DATA_CADASTRO": {"type": DataTypes.TIMESTAMP(), "allowNull": True},
    "ISS_COBRADO_USUARIO": {"type": DataTypes.STRING(1), "allowNull": True},
    "CONCILIADO": {"type": DataTypes.STRING(1), "allowNull": True},
    "TIPO_ATO": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "NLOTE": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "APONTAMENTO_PROTESTO": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "VALOR_ATO": {"type": DataTypes.NUMERIC(14, 3), "allowNull": True},
    "NUMERO_LIVRO": {"type": DataTypes.STRING(30), "allowNull": True},
    "NUMERO_FOLHAS": {"type": DataTypes.STRING(30), "allowNull": True},
    "VALOR_INFORMACOES_CENTRAIS": {"type": DataTypes.NUMERIC(14, 3), "allowNull": True},
    "ENVIO_IMEDIATO": {"type": DataTypes.STRING(1), "allowNull": True},
    "PROTOCOLO": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "CPFCNPJ": {"type": DataTypes.STRING(15), "allowNull": True},
    "CARTORIO_ORIGEM": {"type": DataTypes.STRING(10), "allowNull": True},
    "STATUS_RET_EXPORT": {"type": DataTypes.STRING(3), "allowNull": True},
    "MENSAGEM_RET_EXPORT": {"type": DataTypes.BLOB_BINARY(), "allowNull": True},
    "EMOLUMENTO_ITEM_ID": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "NUMERO_SELO": {"type": DataTypes.STRING(60), "allowNull": True},
    "SITUACAO_DIFERIDO": {"type": DataTypes.STRING(1), "allowNull": True},
    "DATA_INUTILIZACAO": {"type": DataTypes.TIMESTAMP(), "allowNull": True},
    "SELO_PROTOCOLO": {"type": DataTypes.STRING(1), "allowNull": True},
    "VALOR_FUNDO_SELO": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "INTEIRO_TEOR_TEXTO": {"type": DataTypes.BLOB_BINARY(), "allowNull": True},
    "TIPO_ENVOLVIDO": {"type": DataTypes.STRING(150), "allowNull": True},
    "IDAP": {"type": DataTypes.STRING(150), "allowNull": True},
    "FUNDO_SELO": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "DISTRIBUIDOR": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "DATA_IMPORTACAO": {"type": DataTypes.TIMESTAMP(), "allowNull": True},
    "SELO_RETIFICADO": {"type": DataTypes.STRING(60), "allowNull": True},
}

G_SELO_LIVRO_OPTIONS: dict[str, Any] = {
    "tableName": G_SELO_LIVRO_TABLE,
    "primaryKey": "SELO_LIVRO_ID",
}


@lru_cache(maxsize=1)
def get_g_selo_livro_model() -> Type[Any]:
    orm = get_orm()

    existing = orm.models.get(G_SELO_LIVRO_MODEL_NAME) or orm.models.get(G_SELO_LIVRO_TABLE)
    if existing is not None:
        return existing

    return orm.define(
        G_SELO_LIVRO_MODEL_NAME,
        G_SELO_LIVRO_ATTRIBUTES,
        G_SELO_LIVRO_OPTIONS,
    )
