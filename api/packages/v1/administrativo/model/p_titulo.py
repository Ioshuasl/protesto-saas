from __future__ import annotations

from functools import lru_cache
from typing import Any, Type

from orm_py import DataTypes

from database.orm_firebird import get_orm

P_TITULO_TABLE = "P_TITULO"
P_TITULO_MODEL_NAME = "P_TITULO"

# P_TITULO — títulos de protesto
# Gerado a partir de QueryInterface.describe_table (Firebird santarita).

P_TITULO_ATTRIBUTES: dict[str, dict[str, Any]] = {
    "TITULO_ID": {"type": DataTypes.NUMERIC(10, 0), "primaryKey": True, "autoIncrement": False, "allowNull": False},
    "DATA_APONTAMENTO": {"type": DataTypes.TIMESTAMP(), "allowNull": True},
    "LOCAL_ACEITE": {"type": DataTypes.STRING(150), "allowNull": True},
    "DATA_ACEITE": {"type": DataTypes.TIMESTAMP(), "allowNull": True},
    "PRAZO": {"type": DataTypes.STRING(15), "allowNull": True},
    "VALOR_TITULO": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "DATA_PROTESTO": {"type": DataTypes.TIMESTAMP(), "allowNull": True},
    "DATA_CANCELAMENTO": {"type": DataTypes.TIMESTAMP(), "allowNull": True},
    "OBSERVACOES": {"type": DataTypes.STRING(260), "allowNull": True},
    "ESPECIE_ID": {"type": DataTypes.NUMERIC(10, 0), "allowNull": True},
    "OCORRENCIA_ID": {"type": DataTypes.NUMERIC(10, 0), "allowNull": True},
    "NUMERO_TITULO": {"type": DataTypes.STRING(30), "allowNull": True},
    "DATA_VENCIMENTO_TITULO": {"type": DataTypes.TIMESTAMP(), "allowNull": True},
    "DATA_EMISSAO_TITULO": {"type": DataTypes.TIMESTAMP(), "allowNull": True},
    "MOTIVO_APONTAMENTO_ID": {"type": DataTypes.NUMERIC(10, 0), "allowNull": True},
    "TABELA_EMOLUMENTO_ID": {"type": DataTypes.NUMERIC(10, 0), "allowNull": True},
    "VALOR_EMOLUMENTO": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "VALOR_TAXA_JUDICIARIA": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "VALOR_TAXA_INTIMACAO": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "VALOR_DESCONTO": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "VALOR_TAXA_EDITAL": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "VALOR_TAXA_JUROS": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "NUMERO_APONTAMENTO": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "DATA_CADASTRO": {"type": DataTypes.TIMESTAMP(), "allowNull": True},
    "MOTIVO_CANCELAMENTO": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "DATA_SUSTADO": {"type": DataTypes.TIMESTAMP(), "allowNull": True},
    "FOLHA_APONTAMENTO": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "LIVRO_ID_APONTAMENTO": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "TIPO_ACEITE": {"type": DataTypes.STRING(2), "allowNull": True},
    "USER_ASSINA_PROT": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "LIVRO_ID_PROTESTO": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "FOLHA_PROTESTO": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "USER_ASSINA_APONT": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "DATA_PAGO": {"type": DataTypes.TIMESTAMP(), "allowNull": True},
    "VALOR_TAXA_CORREIOS": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "DATA_ENV_SERASA": {"type": DataTypes.TIMESTAMP(), "allowNull": True},
    "DATA_RET_SERASA": {"type": DataTypes.TIMESTAMP(), "allowNull": True},
    "VALOR_TAXA_CANCEL": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "VALOR_TAXA_AVERB": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "DATA_DESISTENCIA": {"type": DataTypes.TIMESTAMP(), "allowNull": True},
    "NUMERO_CANCELAMENTO": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "NUMERO_PROTESTO": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "NUMERO_AR": {"type": DataTypes.STRING(30), "allowNull": True},
    "SITUACAO_ACEITE": {"type": DataTypes.STRING(60), "allowNull": True},
    "PESSOA_ACEITOU": {"type": DataTypes.STRING(150), "allowNull": True},
    "AGENCIA_CORREIO": {"type": DataTypes.STRING(60), "allowNull": True},
    "TAXA_CORRECAO": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "NUMERO_LIVRO_APONT": {"type": DataTypes.STRING(15), "allowNull": True},
    "NUMERO_TITULO_BANCO": {"type": DataTypes.STRING(30), "allowNull": True},
    "PRACA_PAGAMENTO": {"type": DataTypes.STRING(60), "allowNull": True},
    "DATA_MOV_SERASA": {"type": DataTypes.TIMESTAMP(), "allowNull": True},
    "TIPO_ENDOSSO": {"type": DataTypes.STRING(2), "allowNull": True},
    "NOSSO_NUMERO": {"type": DataTypes.STRING(30), "allowNull": True},
    "VALOR_TAXA_FUNDESP": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "COBRAR_JUROS": {"type": DataTypes.STRING(2), "allowNull": True},
    "EMOLUMENTO_ITEM_ID": {"type": DataTypes.NUMERIC(10, 0), "allowNull": True},
    "DATA_INTIMACAO": {"type": DataTypes.TIMESTAMP(), "allowNull": True},
    "DATA_VENCIMENTO_BOLETO": {"type": DataTypes.TIMESTAMP(), "allowNull": True},
    "VALOR_TOTAL": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "LETRA_FOLHA": {"type": DataTypes.STRING(2), "allowNull": True},
    "PAGAMENTO_POSTERIOR": {"type": DataTypes.STRING(2), "allowNull": True},
    "VALOR_ISS": {"type": DataTypes.NUMERIC(14, 3), "allowNull": True},
    "SERVICO_GRATUITO": {"type": DataTypes.STRING(2), "allowNull": True},
    "MOTIVO_ISENCAO": {"type": DataTypes.STRING(150), "allowNull": True},
    "PAGAMENTO_DIFERIDO": {"type": DataTypes.STRING(2), "allowNull": True},
    "TITULO_ANTIGO": {"type": DataTypes.STRING(2), "allowNull": True},
    "NLOTE": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "FORMA_PAGAMENTO": {"type": DataTypes.STRING(2), "allowNull": True},
    "VALOR_TOTAL_CUSTAS": {"type": DataTypes.NUMERIC(14, 3), "allowNull": True},
    "AGENCIA_CODIGO_CEDENTE": {"type": DataTypes.STRING(15), "allowNull": True},
    "AGENCIA_CENTRALIZADORA": {"type": DataTypes.STRING(10), "allowNull": True},
    "STATUS_IMPORTACAO": {"type": DataTypes.STRING(2), "allowNull": True},
    "BANCO_ID": {"type": DataTypes.NUMERIC(10, 0), "allowNull": True},
    "CODIGO_PRACA": {"type": DataTypes.STRING(10), "allowNull": True},
    "PROTESTADO": {"type": DataTypes.STRING(2), "allowNull": True},
    "SELECAO_STATUS": {"type": DataTypes.STRING(2), "allowNull": True},
    "IMPORTAR": {"type": DataTypes.STRING(2), "allowNull": True},
    "NFSE_ID": {"type": DataTypes.NUMERIC(10, 0), "allowNull": True},
    "DATA_RETORNO_CDA": {"type": DataTypes.TIMESTAMP(), "allowNull": True},
    "ARQUIVO_TITULO_ID": {"type": DataTypes.NUMERIC(10, 0), "allowNull": True},
    "EMAIL": {"type": DataTypes.STRING(260), "allowNull": True},
    "DATA_ANUENCIA": {"type": DataTypes.TIMESTAMP(), "allowNull": True},
    "ORIGEM_ANUENCIA": {"type": DataTypes.STRING(3), "allowNull": True},
    "APRESENTANTE_PERMITIDO": {"type": DataTypes.STRING(2), "allowNull": True},
    "CEDENTE_PERMITIDO": {"type": DataTypes.STRING(2), "allowNull": True},
    "CREDOR_PERMITIDO": {"type": DataTypes.STRING(2), "allowNull": True},
    "ANUENCIA": {"type": DataTypes.STRING(2), "allowNull": True},
    "SITUACAO_CENPROT": {"type": DataTypes.STRING(2), "allowNull": True},
    "CUSTAS_CANCELAMENTO_ID": {"type": DataTypes.NUMERIC(10, 0), "allowNull": True},
    "CHAVE_IMPORTACAO": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "IMPSITUACAO_TITULO": {"type": DataTypes.STRING(30), "allowNull": True},
    "LIVRO_PAGAMENTO": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "LETRA_LIVRO_PAGAMENTO": {"type": DataTypes.STRING(3), "allowNull": True},
    "FOLHA_LIVRO_PAGAMENTO": {"type": DataTypes.NUMERIC(10, 2), "allowNull": True},
    "CHAVE_UNICA_CENPROT": {"type": DataTypes.STRING(150), "allowNull": True},
    "PROTESTO_ARTIGO_9": {"type": DataTypes.STRING(2), "allowNull": True},
    "OCORRENCIA_ANDAMENTO_ID": {"type": DataTypes.NUMERIC(10, 0), "allowNull": True},
}

P_TITULO_OPTIONS: dict[str, Any] = {
    "tableName": P_TITULO_TABLE,
    "primaryKey": "TITULO_ID",
}


@lru_cache(maxsize=1)
def get_p_titulo_model() -> Type[Any]:
    orm = get_orm()

    existing = orm.models.get(P_TITULO_MODEL_NAME) or orm.models.get(P_TITULO_TABLE)
    if existing is not None:
        return existing

    return orm.define(
        P_TITULO_MODEL_NAME,
        P_TITULO_ATTRIBUTES,
        P_TITULO_OPTIONS,
    )
