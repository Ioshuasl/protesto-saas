from __future__ import annotations

from functools import lru_cache
from typing import Any, Type

from orm_py import DataTypes

from database.orm_firebird import get_orm

P_OCORRENCIAS_TABLE = "P_OCORRENCIAS"
P_OCORRENCIAS_MODEL_NAME = "P_OCORRENCIAS"

# P_OCORRENCIAS — cadastro de ocorrências/status para andamento do título
# Introspecção QueryInterface.describe_table (Firebird santarita) + amostra 2026-05:
#   OCORRENCIAS_ID — NUMERIC(10,0), PK (valores inteiros 1..n; gaps possíveis ex.: 9)
#   CODIGO         — VARCHAR(10): numérico ("1","2") ou alfanumérico ("A","B")
#   DESCRICAO      — VARCHAR(260)
#   TIPO           — VARCHAR(30): vazio permitido; API valida gravação em:
#     CADASTRO, APONTADO, INTIMACAO, ACEITE, DESISTENCIA, PAGAMENTO, CANCELAMENTO
#     (legado no banco: CANC/PAGTO, PROTESTO, etc. — leitura sem conversão)
# FK: P_TITULO.OCORRENCIA_ID → OCORRENCIAS_ID
# FK: P_PESSOA_VINCULO.OCORRENCIA_ID → OCORRENCIAS_ID

P_OCORRENCIAS_ATTRIBUTES: dict[str, dict[str, Any]] = {
    "OCORRENCIAS_ID": {
        "type": DataTypes.NUMERIC(10, 0),
        "primaryKey": True,
        "autoIncrement": False,
        "allowNull": False,
    },
    "CODIGO": {"type": DataTypes.STRING(10), "allowNull": True},
    "DESCRICAO": {"type": DataTypes.STRING(260), "allowNull": True},
    "TIPO": {"type": DataTypes.STRING(30), "allowNull": True},
}

P_OCORRENCIAS_OPTIONS: dict[str, Any] = {
    "tableName": P_OCORRENCIAS_TABLE,
    "primaryKey": "OCORRENCIAS_ID",
}


@lru_cache(maxsize=1)
def get_p_ocorrencias_model() -> Type[Any]:
    orm = get_orm()

    existing = orm.models.get(P_OCORRENCIAS_MODEL_NAME) or orm.models.get(
        P_OCORRENCIAS_TABLE
    )
    if existing is not None:
        return existing

    return orm.define(
        P_OCORRENCIAS_MODEL_NAME,
        P_OCORRENCIAS_ATTRIBUTES,
        P_OCORRENCIAS_OPTIONS,
    )
