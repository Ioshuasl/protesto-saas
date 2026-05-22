from __future__ import annotations

from functools import lru_cache
from typing import Any, Type

from orm_py import DataTypes

from database.orm_firebird import get_orm

G_USUARIO_TABLE = "G_USUARIO"
G_USUARIO_MODEL_NAME = "G_USUARIO"

# G_USUARIO — cadastro de usuários do sistema
# DDL Firebird: NUMERICO = NUMERIC(10,2); VARCHAR_001 = VARCHAR(1); etc.

G_USUARIO_ATTRIBUTES: dict[str, dict[str, Any]] = {
    "USUARIO_ID": {
        "type": DataTypes.NUMERIC(10, 2),
        "primaryKey": True,
        "autoIncrement": False,
        "allowNull": False,
    },
    "TROCARSENHA": {"type": DataTypes.STRING(2), "allowNull": True},
    "LOGIN": {"type": DataTypes.STRING(30), "allowNull": True},
    "SENHA": {"type": DataTypes.STRING(60), "allowNull": True},
    "SITUACAO": {"type": DataTypes.STRING(2), "allowNull": True},
    "NOME_COMPLETO": {"type": DataTypes.STRING(150), "allowNull": True},
    "FUNCAO": {"type": DataTypes.STRING(60), "allowNull": True},
    "ASSINA": {"type": DataTypes.STRING(2), "allowNull": True},
    "SIGLA": {"type": DataTypes.STRING(10), "allowNull": True},
    "USUARIO_TAB": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "ULTIMO_LOGIN": {"type": DataTypes.TIMESTAMP(), "allowNull": True},
    "ULTIMO_LOGIN_REGS": {"type": DataTypes.TIMESTAMP(), "allowNull": True},
    "DATA_EXPIRACAO": {"type": DataTypes.TIMESTAMP(), "allowNull": True},
    "SENHA_ANTERIOR": {"type": DataTypes.STRING(150), "allowNull": True},
    "ANDAMENTO_PADRAO": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "LEMBRETE_PERGUNTA": {"type": DataTypes.STRING(60), "allowNull": True},
    "LEMBRETE_RESPOSTA": {"type": DataTypes.STRING(60), "allowNull": True},
    "ANDAMENTO_PADRAO2": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "RECEBER_MENSAGEM_ARROLAMENTO": {"type": DataTypes.STRING(2), "allowNull": True},
    "EMAIL": {"type": DataTypes.STRING(260), "allowNull": True},
    "ASSINA_CERTIDAO": {"type": DataTypes.STRING(2), "allowNull": True},
    "RECEBER_EMAIL_PENHORA": {"type": DataTypes.STRING(2), "allowNull": True},
    "FOTO": {"type": DataTypes.BLOB_BINARY(), "allowNull": True},
    "NAO_RECEBER_CHAT_TODOS": {"type": DataTypes.STRING(2), "allowNull": True},
    "PODE_ALTERAR_CAIXA": {"type": DataTypes.STRING(2), "allowNull": True},
    "RECEBER_CHAT_CERTIDAO_ONLINE": {"type": DataTypes.STRING(2), "allowNull": True},
    "RECEBER_CHAT_CANCELAMENTO": {"type": DataTypes.STRING(2), "allowNull": True},
    "CPF": {"type": DataTypes.STRING(15), "allowNull": True},
    "SOMENTE_LEITURA": {"type": DataTypes.STRING(2), "allowNull": True},
    "RECEBER_CHAT_ENVIO_ONR": {"type": DataTypes.STRING(2), "allowNull": True},
    "TIPO_USUARIO": {"type": DataTypes.STRING(3), "allowNull": True},
    "DISTRIBUIR_PROTOCOLO_RI": {"type": DataTypes.STRING(3), "allowNull": True},
    "ULTIMO_PROTOCOLO_RI": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "SENHA_API": {"type": DataTypes.STRING(260), "allowNull": True},
}

G_USUARIO_OPTIONS: dict[str, Any] = {
    "tableName": G_USUARIO_TABLE,
    "primaryKey": "USUARIO_ID",
}


@lru_cache(maxsize=1)
def get_g_usuario_model() -> Type[Any]:
    orm = get_orm()

    existing = orm.models.get(G_USUARIO_MODEL_NAME) or orm.models.get(G_USUARIO_TABLE)
    if existing is not None:
        return existing

    return orm.define(
        G_USUARIO_MODEL_NAME,
        G_USUARIO_ATTRIBUTES,
        G_USUARIO_OPTIONS,
    )
