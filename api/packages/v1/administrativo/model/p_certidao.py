from __future__ import annotations

from functools import lru_cache
from typing import Any, Type

from orm_py import DataTypes

from database.orm_firebird import get_orm

P_CERTIDAO_TABLE = "P_CERTIDAO"
P_CERTIDAO_MODEL_NAME = "P_CERTIDAO"

# Domínio Firebird (describe_table + amostra 2026-05-26):
#   TIPO_CERTIDAO — R = certidão Serasa; P = certidão positiva; N = certidão negativa
#   TIPO_REMESSA  — usado quando TIPO_CERTIDAO = R:
#                   P = certidão de protesto do Serasa; C = certidão de cancelamento do Serasa
#                   NULL quando TIPO_CERTIDAO = P ou N
#   STATUS        — A = ativo; C = cancelado
# FKs:
#   USUARIO_ID          -> G_USUARIO.USUARIO_ID
#   NFSE_ID             -> C_NFSE.NFSE_ID
#   PROTECAO_CREDITO_ID -> P_PROTECAO_CREDITO.PROTECAO_CREDITO_ID

P_CERTIDAO_ATTRIBUTES: dict[str, dict[str, Any]] = {
    "CERTIDAO_ID": {
        "type": DataTypes.NUMERIC(10, 0),
        "primaryKey": True,
        "autoIncrement": False,
        "allowNull": False,
    },
    "USUARIO_ID": {"type": DataTypes.NUMERIC(10, 0), "allowNull": True},
    "DATA_CERTIDAO": {"type": DataTypes.TIMESTAMP(), "allowNull": True},
    "HORA_CERTIDAO": {"type": DataTypes.STRING(10), "allowNull": True},
    "TIPO_CERTIDAO": {"type": DataTypes.STRING(1), "allowNull": True},
    "VALOR_EMOLUMENTO": {"type": DataTypes.NUMERIC(14, 3), "allowNull": True},
    "VALOR_TAXA_JUDICIARIA": {
        "type": DataTypes.NUMERIC(14, 3),
        "allowNull": True,
    },
    "VALOR_FUNDESP": {"type": DataTypes.NUMERIC(14, 3), "allowNull": True},
    "VALOR_TAXA_EXTRA": {"type": DataTypes.NUMERIC(14, 3), "allowNull": True},
    "NUMERO_IMPRESSAO": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "CPFCNPJ": {"type": DataTypes.STRING(15), "allowNull": True},
    "NOME": {"type": DataTypes.STRING(150), "allowNull": True},
    "STATUS": {"type": DataTypes.STRING(1), "allowNull": True},
    "OBSERVACAO": {"type": DataTypes.BLOB_BINARY(), "allowNull": True},
    "VALOR_TAXA_ISS": {"type": DataTypes.NUMERIC(14, 3), "allowNull": True},
    "APRESENTANTE": {"type": DataTypes.STRING(150), "allowNull": True},
    "NFSE_ID": {"type": DataTypes.NUMERIC(10, 0), "allowNull": True},
    "QTD_PROTESTOS": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "QTD_CANCELADOS": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "QTD_SUSTADO": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "N_REMESSA": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "TIPO_REMESSA": {"type": DataTypes.STRING(1), "allowNull": True},
    "PROTECAO_CREDITO_ID": {"type": DataTypes.NUMERIC(10, 0), "allowNull": True},
}

P_CERTIDAO_OPTIONS: dict[str, Any] = {
    "tableName": P_CERTIDAO_TABLE,
    "primaryKey": "CERTIDAO_ID",
}


@lru_cache(maxsize=1)
def get_p_certidao_model() -> Type[Any]:
    orm = get_orm()

    existing = orm.models.get(P_CERTIDAO_MODEL_NAME) or orm.models.get(P_CERTIDAO_TABLE)
    if existing is not None:
        return existing

    return orm.define(
        P_CERTIDAO_MODEL_NAME,
        P_CERTIDAO_ATTRIBUTES,
        P_CERTIDAO_OPTIONS,
    )
