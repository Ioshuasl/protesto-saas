from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Any, Mapping, Optional, Union

from pydantic import BaseModel, ConfigDict, field_validator

from actions.validations.text import Text

# VARCHAR(2) — padrão protesto S/N
SIM_CODIGO = "S"
NAO_CODIGO = "N"
SIM_NAO_CODIGOS = frozenset({SIM_CODIGO, NAO_CODIGO})

SELECAO_STATUS_CODIGO = "I"

TIPO_ACEITE_CODIGOS = frozenset({"A", "E"})
TIPO_ENDOSSO_CODIGOS = frozenset({"M", "T"})
STATUS_IMPORTACAO_CODIGOS = frozenset({"D", "E"})

_NUMERIC_INT_KEYS = frozenset(
    {
        "titulo_id",
        "especie_id",
        "ocorrencia_id",
        "motivo_apontamento_id",
        "tabela_emolumento_id",
        "banco_id",
        "nfse_id",
        "arquivo_titulo_id",
        "custas_cancelamento_id",
        "ocorrencia_andamento_id",
        "emolumento_item_id",
    }
)

_NUMERIC_FLOAT_KEYS = frozenset(
    {
        "valor_titulo",
        "valor_emolumento",
        "valor_taxa_judiciaria",
        "valor_taxa_intimacao",
        "valor_desconto",
        "valor_taxa_edital",
        "valor_taxa_juros",
        "numero_apontamento",
        "motivo_cancelamento",
        "folha_apontamento",
        "livro_id_apontamento",
        "user_assina_prot",
        "livro_id_protesto",
        "folha_protesto",
        "user_assina_apont",
        "valor_taxa_correios",
        "valor_taxa_cancel",
        "valor_taxa_averb",
        "numero_cancelamento",
        "numero_protesto",
        "taxa_correcao",
        "valor_taxa_fundesp",
        "valor_total",
        "valor_iss",
        "nlote",
        "valor_total_custas",
        "chave_importacao",
        "livro_pagamento",
        "folha_livro_pagamento",
    }
)

TITULO_API_TO_DB: dict[str, str] = {
    "titulo_id": "TITULO_ID",
    "data_apontamento": "DATA_APONTAMENTO",
    "local_aceite": "LOCAL_ACEITE",
    "data_aceite": "DATA_ACEITE",
    "prazo": "PRAZO",
    "valor_titulo": "VALOR_TITULO",
    "data_protesto": "DATA_PROTESTO",
    "data_cancelamento": "DATA_CANCELAMENTO",
    "observacoes": "OBSERVACOES",
    "especie_id": "ESPECIE_ID",
    "ocorrencia_id": "OCORRENCIA_ID",
    "numero_titulo": "NUMERO_TITULO",
    "data_vencimento_titulo": "DATA_VENCIMENTO_TITULO",
    "data_emissao_titulo": "DATA_EMISSAO_TITULO",
    "motivo_apontamento_id": "MOTIVO_APONTAMENTO_ID",
    "tabela_emolumento_id": "TABELA_EMOLUMENTO_ID",
    "valor_emolumento": "VALOR_EMOLUMENTO",
    "valor_taxa_judiciaria": "VALOR_TAXA_JUDICIARIA",
    "valor_taxa_intimacao": "VALOR_TAXA_INTIMACAO",
    "valor_desconto": "VALOR_DESCONTO",
    "valor_taxa_edital": "VALOR_TAXA_EDITAL",
    "valor_taxa_juros": "VALOR_TAXA_JUROS",
    "numero_apontamento": "NUMERO_APONTAMENTO",
    "data_cadastro": "DATA_CADASTRO",
    "motivo_cancelamento": "MOTIVO_CANCELAMENTO",
    "data_sustado": "DATA_SUSTADO",
    "folha_apontamento": "FOLHA_APONTAMENTO",
    "livro_id_apontamento": "LIVRO_ID_APONTAMENTO",
    "tipo_aceite": "TIPO_ACEITE",
    "user_assina_prot": "USER_ASSINA_PROT",
    "livro_id_protesto": "LIVRO_ID_PROTESTO",
    "folha_protesto": "FOLHA_PROTESTO",
    "user_assina_apont": "USER_ASSINA_APONT",
    "data_pago": "DATA_PAGO",
    "valor_taxa_correios": "VALOR_TAXA_CORREIOS",
    "data_env_serasa": "DATA_ENV_SERASA",
    "data_ret_serasa": "DATA_RET_SERASA",
    "valor_taxa_cancel": "VALOR_TAXA_CANCEL",
    "valor_taxa_averb": "VALOR_TAXA_AVERB",
    "data_desistencia": "DATA_DESISTENCIA",
    "numero_cancelamento": "NUMERO_CANCELAMENTO",
    "numero_protesto": "NUMERO_PROTESTO",
    "numero_ar": "NUMERO_AR",
    "situacao_aceite": "SITUACAO_ACEITE",
    "pessoa_aceitou": "PESSOA_ACEITOU",
    "agencia_correio": "AGENCIA_CORREIO",
    "taxa_correcao": "TAXA_CORRECAO",
    "numero_livro_apont": "NUMERO_LIVRO_APONT",
    "numero_titulo_banco": "NUMERO_TITULO_BANCO",
    "praca_pagamento": "PRACA_PAGAMENTO",
    "data_mov_serasa": "DATA_MOV_SERASA",
    "tipo_endosso": "TIPO_ENDOSSO",
    "nosso_numero": "NOSSO_NUMERO",
    "valor_taxa_fundesp": "VALOR_TAXA_FUNDESP",
    "cobrar_juros": "COBRAR_JUROS",
    "emolumento_item_id": "EMOLUMENTO_ITEM_ID",
    "data_intimacao": "DATA_INTIMACAO",
    "data_vencimento_boleto": "DATA_VENCIMENTO_BOLETO",
    "valor_total": "VALOR_TOTAL",
    "letra_folha": "LETRA_FOLHA",
    "pagamento_posterior": "PAGAMENTO_POSTERIOR",
    "valor_iss": "VALOR_ISS",
    "servico_gratuito": "SERVICO_GRATUITO",
    "motivo_isencao": "MOTIVO_ISENCAO",
    "pagamento_diferido": "PAGAMENTO_DIFERIDO",
    "titulo_antigo": "TITULO_ANTIGO",
    "nlote": "NLOTE",
    "forma_pagamento": "FORMA_PAGAMENTO",
    "valor_total_custas": "VALOR_TOTAL_CUSTAS",
    "agencia_codigo_cedente": "AGENCIA_CODIGO_CEDENTE",
    "agencia_centralizadora": "AGENCIA_CENTRALIZADORA",
    "status_importacao": "STATUS_IMPORTACAO",
    "banco_id": "BANCO_ID",
    "codigo_praca": "CODIGO_PRACA",
    "protestado": "PROTESTADO",
    "selecao_status": "SELECAO_STATUS",
    "importar": "IMPORTAR",
    "nfse_id": "NFSE_ID",
    "data_retorno_cda": "DATA_RETORNO_CDA",
    "arquivo_titulo_id": "ARQUIVO_TITULO_ID",
    "email": "EMAIL",
    "data_anuencia": "DATA_ANUENCIA",
    "origem_anuencia": "ORIGEM_ANUENCIA",
    "apresentante_permitido": "APRESENTANTE_PERMITIDO",
    "cedente_permitido": "CEDENTE_PERMITIDO",
    "credor_permitido": "CREDOR_PERMITIDO",
    "anuencia": "ANUENCIA",
    "situacao_cenprot": "SITUACAO_CENPROT",
    "custas_cancelamento_id": "CUSTAS_CANCELAMENTO_ID",
    "chave_importacao": "CHAVE_IMPORTACAO",
    "impsituacao_titulo": "IMPSITUACAO_TITULO",
    "livro_pagamento": "LIVRO_PAGAMENTO",
    "letra_livro_pagamento": "LETRA_LIVRO_PAGAMENTO",
    "folha_livro_pagamento": "FOLHA_LIVRO_PAGAMENTO",
    "chave_unica_cenprot": "CHAVE_UNICA_CENPROT",
    "protesto_artigo_9": "PROTESTO_ARTIGO_9",
    "ocorrencia_andamento_id": "OCORRENCIA_ANDAMENTO_ID",
}


def normalize_sim_nao(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    normalized = str(value).strip().upper()
    if not normalized:
        return NAO_CODIGO
    if normalized not in SIM_NAO_CODIGOS:
        raise ValueError(f"Valor inválido: '{value}'. Use S (sim) ou N (não).")
    return normalized


def normalize_sim_nao_from_db(value: Optional[str]) -> Optional[str]:
    if value is None or not str(value).strip():
        return NAO_CODIGO
    normalized = str(value).strip().upper()
    return SIM_CODIGO if normalized == SIM_CODIGO else NAO_CODIGO


def normalize_tipo_aceite(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    normalized = str(value).strip().upper()
    if not normalized:
        return None
    if normalized not in TIPO_ACEITE_CODIGOS:
        raise ValueError(f"Tipo de aceite inválido: '{value}'. Use A ou E.")
    return normalized


def normalize_tipo_endosso(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    normalized = str(value).strip().upper()
    if not normalized:
        return None
    if normalized not in TIPO_ENDOSSO_CODIGOS:
        raise ValueError(f"Tipo de endosso inválido: '{value}'. Use M ou T.")
    return normalized


def normalize_status_importacao(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    normalized = str(value).strip().upper()
    if not normalized:
        return None
    if normalized not in STATUS_IMPORTACAO_CODIGOS:
        raise ValueError(f"Status de importação inválido: '{value}'. Use D ou E.")
    return normalized


def normalize_selecao_status_from_db(_value: Optional[str]) -> str:
    return SELECAO_STATUS_CODIGO


def titulo_schema_to_orm_payload(
    data: Mapping[str, Any],
    *,
    force_selecao_status: bool = True,
) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    for api_key, db_key in TITULO_API_TO_DB.items():
        if api_key == "titulo_id":
            continue
        if api_key not in data:
            continue
        value = data[api_key]
        if value is None:
            continue
        payload[db_key] = value
    if force_selecao_status:
        payload["SELECAO_STATUS"] = SELECAO_STATUS_CODIGO
    return payload


class POcorrenciasNestedSchema(BaseModel):
    ocorrencias_id: Optional[int] = None
    codigo: Optional[str] = None
    descricao: Optional[str] = None
    tipo: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class PEspecieIndexNestedSchema(BaseModel):
    especie_id: Optional[int] = None
    especie: Optional[str] = None
    descricao: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class POcorrenciaIndexNestedSchema(BaseModel):
    ocorrencias_id: Optional[int] = None
    descricao: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class PBancoIndexNestedSchema(BaseModel):
    banco_id: Optional[int] = None
    descricao: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class PTituloIndexItemSchema(BaseModel):
    """Shape enxuto do GET index de p_titulo."""

    titulo_id: Optional[int] = None
    numero_titulo: Optional[str] = None
    nosso_numero: Optional[str] = None
    numero_apontamento: Optional[float] = None
    especie_id: Optional[int] = None
    especie: Optional[PEspecieIndexNestedSchema] = None
    valor_titulo: Optional[float] = None
    ocorrencia_id: Optional[int] = None
    ocorrencia: Optional[POcorrenciaIndexNestedSchema] = None
    banco_id: Optional[int] = None
    banco: Optional[PBancoIndexNestedSchema] = None
    quantidade_pessoas_vinculadas: int = 0
    apresentante_nome: Optional[str] = None
    apresentante_cpfcnpj: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class POcorrenciaAndamentoNestedSchema(BaseModel):
    ocorrencia_andamento_id: Optional[int] = None
    codigo: Optional[str] = None
    descricao: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class PPessoaNestedSchema(BaseModel):
    pessoa_id: Optional[int] = None
    nome: Optional[str] = None
    cpfcnpj: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class PPessoaVinculoNestedSchema(BaseModel):
    pessoa_vinculo_id: Optional[int] = None
    titulo_id: Optional[int] = None
    pessoa_id: Optional[int] = None
    nome: Optional[str] = None
    cpfcnpj: Optional[str] = None
    tipo_vinculo: Optional[str] = None
    pessoa: Optional[PPessoaNestedSchema] = None

    model_config = ConfigDict(from_attributes=True)


class PAndamentoNestedSchema(BaseModel):
    andamento_id: Optional[int] = None
    titulo_id: Optional[int] = None
    ocorrencia_andamento_id: Optional[int] = None
    data_ocorrencia: Optional[Union[datetime, date]] = None
    data_geracao: Optional[Union[datetime, date]] = None
    usuario_id: Optional[int] = None
    arquivo_gerado: Optional[str] = None
    ocorrencia_andamento: Optional[POcorrenciaAndamentoNestedSchema] = None

    model_config = ConfigDict(from_attributes=True)


class PTituloSchema(BaseModel):
    titulo_id: Optional[int] = None
    data_apontamento: Optional[Union[datetime, date]] = None
    local_aceite: Optional[str] = None
    data_aceite: Optional[Union[datetime, date]] = None
    prazo: Optional[str] = None
    valor_titulo: Optional[float] = None
    data_protesto: Optional[Union[datetime, date]] = None
    data_cancelamento: Optional[Union[datetime, date]] = None
    observacoes: Optional[str] = None
    especie_id: Optional[int] = None
    ocorrencia_id: Optional[int] = None
    numero_titulo: Optional[str] = None
    data_vencimento_titulo: Optional[Union[datetime, date]] = None
    data_emissao_titulo: Optional[Union[datetime, date]] = None
    motivo_apontamento_id: Optional[int] = None
    tabela_emolumento_id: Optional[int] = None
    valor_emolumento: Optional[float] = None
    valor_taxa_judiciaria: Optional[float] = None
    valor_taxa_intimacao: Optional[float] = None
    valor_desconto: Optional[float] = None
    valor_taxa_edital: Optional[float] = None
    valor_taxa_juros: Optional[float] = None
    numero_apontamento: Optional[float] = None
    data_cadastro: Optional[Union[datetime, date]] = None
    motivo_cancelamento: Optional[float] = None
    data_sustado: Optional[Union[datetime, date]] = None
    folha_apontamento: Optional[float] = None
    livro_id_apontamento: Optional[float] = None
    tipo_aceite: Optional[str] = None
    user_assina_prot: Optional[float] = None
    livro_id_protesto: Optional[float] = None
    folha_protesto: Optional[float] = None
    user_assina_apont: Optional[float] = None
    data_pago: Optional[Union[datetime, date]] = None
    valor_taxa_correios: Optional[float] = None
    data_env_serasa: Optional[Union[datetime, date]] = None
    data_ret_serasa: Optional[Union[datetime, date]] = None
    valor_taxa_cancel: Optional[float] = None
    valor_taxa_averb: Optional[float] = None
    data_desistencia: Optional[Union[datetime, date]] = None
    numero_cancelamento: Optional[float] = None
    numero_protesto: Optional[float] = None
    numero_ar: Optional[str] = None
    situacao_aceite: Optional[str] = None
    pessoa_aceitou: Optional[str] = None
    agencia_correio: Optional[str] = None
    taxa_correcao: Optional[float] = None
    numero_livro_apont: Optional[str] = None
    numero_titulo_banco: Optional[str] = None
    praca_pagamento: Optional[str] = None
    data_mov_serasa: Optional[Union[datetime, date]] = None
    tipo_endosso: Optional[str] = None
    nosso_numero: Optional[str] = None
    valor_taxa_fundesp: Optional[float] = None
    cobrar_juros: Optional[str] = None
    emolumento_item_id: Optional[int] = None
    data_intimacao: Optional[Union[datetime, date]] = None
    data_vencimento_boleto: Optional[Union[datetime, date]] = None
    valor_total: Optional[float] = None
    letra_folha: Optional[str] = None
    pagamento_posterior: Optional[str] = None
    valor_iss: Optional[float] = None
    servico_gratuito: Optional[str] = None
    motivo_isencao: Optional[str] = None
    pagamento_diferido: Optional[str] = None
    titulo_antigo: Optional[str] = None
    nlote: Optional[float] = None
    forma_pagamento: Optional[str] = None
    valor_total_custas: Optional[float] = None
    agencia_codigo_cedente: Optional[str] = None
    agencia_centralizadora: Optional[str] = None
    status_importacao: Optional[str] = None
    banco_id: Optional[int] = None
    codigo_praca: Optional[str] = None
    protestado: Optional[str] = None
    selecao_status: Optional[str] = None
    importar: Optional[str] = None
    nfse_id: Optional[int] = None
    data_retorno_cda: Optional[Union[datetime, date]] = None
    arquivo_titulo_id: Optional[int] = None
    email: Optional[str] = None
    data_anuencia: Optional[Union[datetime, date]] = None
    origem_anuencia: Optional[str] = None
    apresentante_permitido: Optional[str] = None
    cedente_permitido: Optional[str] = None
    credor_permitido: Optional[str] = None
    anuencia: Optional[str] = None
    situacao_cenprot: Optional[str] = None
    custas_cancelamento_id: Optional[int] = None
    chave_importacao: Optional[float] = None
    impsituacao_titulo: Optional[str] = None
    livro_pagamento: Optional[float] = None
    letra_livro_pagamento: Optional[str] = None
    folha_livro_pagamento: Optional[float] = None
    chave_unica_cenprot: Optional[str] = None
    protesto_artigo_9: Optional[str] = None
    ocorrencia_andamento_id: Optional[int] = None
    ocorrencia: Optional[POcorrenciasNestedSchema] = None
    ocorrencia_andamento: Optional[POcorrenciaAndamentoNestedSchema] = None
    pessoa_vinculos: Optional[list[PPessoaVinculoNestedSchema]] = None
    andamentos: Optional[list[PAndamentoNestedSchema]] = None

    model_config = ConfigDict(from_attributes=True)


class PTituloIdSchema(BaseModel):
    titulo_id: int


class PTituloIndexSchema(BaseModel):
    """
    busca_pessoa: LIKE em P_PESSOA_VINCULO (nome/cpfcnpj) e P_PESSOA vinculada.
    Demais filtros: campos diretos de P_TITULO.
    """

    busca_pessoa: Optional[str] = None
    numero_apontamento: Optional[float] = None
    nosso_numero: Optional[str] = None
    numero_titulo: Optional[str] = None
    numero_titulo_banco: Optional[str] = None
    ocorrencia_id: Optional[int] = None
    ocorrencia_andamento_id: Optional[int] = None
    banco_id: Optional[int] = None
    especie_id: Optional[int] = None

    model_config = ConfigDict(extra="forbid")

    @field_validator(
        "busca_pessoa",
        "nosso_numero",
        "numero_titulo",
        "numero_titulo_banco",
        mode="before",
    )
    @classmethod
    def sanitize_text_filters(cls, value):
        if value is None or value == "":
            return None
        return Text.sanitize_input(str(value))

    @field_validator(
        "numero_apontamento",
        "ocorrencia_id",
        "ocorrencia_andamento_id",
        "banco_id",
        "especie_id",
        mode="before",
    )
    @classmethod
    def coerce_numeric_filters(cls, value):
        if value is None or value == "":
            return None
        try:
            if isinstance(value, float) and value == int(value):
                return int(value)
            return float(value) if "." in str(value) else int(value)
        except (TypeError, ValueError) as exc:
            raise ValueError("Filtro numérico inválido.") from exc


class PTituloSaveSchema(PTituloSchema):
    model_config = ConfigDict(extra="forbid")

    @field_validator(
        "tipo_aceite",
        "cobrar_juros",
        "pagamento_posterior",
        "servico_gratuito",
        "pagamento_diferido",
        "titulo_antigo",
        "importar",
        "protestado",
        "apresentante_permitido",
        "cedente_permitido",
        "credor_permitido",
        "anuencia",
        mode="before",
    )
    @classmethod
    def validate_sim_nao_optional(cls, value):
        if value is None or value == "":
            return None
        return normalize_sim_nao(str(value))

    @field_validator("tipo_aceite", mode="after")
    @classmethod
    def validate_tipo_aceite_field(cls, value):
        return normalize_tipo_aceite(value)

    @field_validator("tipo_endosso", mode="before")
    @classmethod
    def validate_tipo_endosso_field(cls, value):
        if value is None or value == "":
            return None
        return normalize_tipo_endosso(str(value))

    @field_validator("status_importacao", mode="before")
    @classmethod
    def validate_status_importacao_field(cls, value):
        if value is None or value == "":
            return None
        return normalize_status_importacao(str(value))


class PTituloUpdateSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    data_apontamento: Optional[Union[datetime, date]] = None
    local_aceite: Optional[str] = None
    data_aceite: Optional[Union[datetime, date]] = None
    prazo: Optional[str] = None
    valor_titulo: Optional[float] = None
    data_protesto: Optional[Union[datetime, date]] = None
    data_cancelamento: Optional[Union[datetime, date]] = None
    observacoes: Optional[str] = None
    especie_id: Optional[int] = None
    ocorrencia_id: Optional[int] = None
    numero_titulo: Optional[str] = None
    data_vencimento_titulo: Optional[Union[datetime, date]] = None
    data_emissao_titulo: Optional[Union[datetime, date]] = None
    motivo_apontamento_id: Optional[int] = None
    tabela_emolumento_id: Optional[int] = None
    valor_emolumento: Optional[float] = None
    valor_taxa_judiciaria: Optional[float] = None
    valor_taxa_intimacao: Optional[float] = None
    valor_desconto: Optional[float] = None
    valor_taxa_edital: Optional[float] = None
    valor_taxa_juros: Optional[float] = None
    numero_apontamento: Optional[float] = None
    motivo_cancelamento: Optional[float] = None
    data_sustado: Optional[Union[datetime, date]] = None
    folha_apontamento: Optional[float] = None
    livro_id_apontamento: Optional[float] = None
    tipo_aceite: Optional[str] = None
    livro_id_protesto: Optional[float] = None
    folha_protesto: Optional[float] = None
    data_pago: Optional[Union[datetime, date]] = None
    valor_taxa_correios: Optional[float] = None
    data_env_serasa: Optional[Union[datetime, date]] = None
    data_ret_serasa: Optional[Union[datetime, date]] = None
    valor_taxa_cancel: Optional[float] = None
    valor_taxa_averb: Optional[float] = None
    data_desistencia: Optional[Union[datetime, date]] = None
    numero_cancelamento: Optional[float] = None
    numero_protesto: Optional[float] = None
    numero_ar: Optional[str] = None
    situacao_aceite: Optional[str] = None
    pessoa_aceitou: Optional[str] = None
    agencia_correio: Optional[str] = None
    taxa_correcao: Optional[float] = None
    numero_livro_apont: Optional[str] = None
    numero_titulo_banco: Optional[str] = None
    praca_pagamento: Optional[str] = None
    data_mov_serasa: Optional[Union[datetime, date]] = None
    tipo_endosso: Optional[str] = None
    nosso_numero: Optional[str] = None
    valor_taxa_fundesp: Optional[float] = None
    cobrar_juros: Optional[str] = None
    emolumento_item_id: Optional[int] = None
    data_intimacao: Optional[Union[datetime, date]] = None
    data_vencimento_boleto: Optional[Union[datetime, date]] = None
    valor_total: Optional[float] = None
    letra_folha: Optional[str] = None
    pagamento_posterior: Optional[str] = None
    valor_iss: Optional[float] = None
    servico_gratuito: Optional[str] = None
    motivo_isencao: Optional[str] = None
    pagamento_diferido: Optional[str] = None
    titulo_antigo: Optional[str] = None
    nlote: Optional[float] = None
    forma_pagamento: Optional[str] = None
    valor_total_custas: Optional[float] = None
    agencia_codigo_cedente: Optional[str] = None
    agencia_centralizadora: Optional[str] = None
    status_importacao: Optional[str] = None
    banco_id: Optional[int] = None
    codigo_praca: Optional[str] = None
    protestado: Optional[str] = None
    importar: Optional[str] = None
    nfse_id: Optional[int] = None
    data_retorno_cda: Optional[Union[datetime, date]] = None
    arquivo_titulo_id: Optional[int] = None
    email: Optional[str] = None
    data_anuencia: Optional[Union[datetime, date]] = None
    origem_anuencia: Optional[str] = None
    apresentante_permitido: Optional[str] = None
    cedente_permitido: Optional[str] = None
    credor_permitido: Optional[str] = None
    anuencia: Optional[str] = None
    situacao_cenprot: Optional[str] = None
    custas_cancelamento_id: Optional[int] = None
    chave_importacao: Optional[float] = None
    impsituacao_titulo: Optional[str] = None
    livro_pagamento: Optional[float] = None
    letra_livro_pagamento: Optional[str] = None
    folha_livro_pagamento: Optional[float] = None
    chave_unica_cenprot: Optional[str] = None
    protesto_artigo_9: Optional[str] = None
    ocorrencia_andamento_id: Optional[int] = None

    @field_validator(
        "tipo_aceite",
        "cobrar_juros",
        "pagamento_posterior",
        "servico_gratuito",
        "pagamento_diferido",
        "titulo_antigo",
        "importar",
        "protestado",
        "apresentante_permitido",
        "cedente_permitido",
        "credor_permitido",
        "anuencia",
        mode="before",
    )
    @classmethod
    def validate_sim_nao_optional(cls, value):
        if value is None or value == "":
            return None
        return normalize_sim_nao(str(value))

    @field_validator("tipo_aceite", mode="after")
    @classmethod
    def validate_tipo_aceite_field(cls, value):
        return normalize_tipo_aceite(value)

    @field_validator("tipo_endosso", mode="before")
    @classmethod
    def validate_tipo_endosso_field(cls, value):
        if value is None or value == "":
            return None
        return normalize_tipo_endosso(str(value))

    @field_validator("status_importacao", mode="before")
    @classmethod
    def validate_status_importacao_field(cls, value):
        if value is None or value == "":
            return None
        return normalize_status_importacao(str(value))


def _normalize_string_field(value: Any) -> Optional[str]:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def map_titulo_row(row: Optional[Mapping[str, Any]]) -> Optional[dict[str, Any]]:
    from database.orm_firebird import normalize_row_keys

    mapped = normalize_row_keys(row)
    if mapped is None:
        return None

    for key in _NUMERIC_INT_KEYS:
        value = mapped.get(key)
        if isinstance(value, Decimal):
            mapped[key] = int(value)
        elif isinstance(value, str) and value.strip().isdigit():
            mapped[key] = int(value.strip())

    for key in _NUMERIC_FLOAT_KEYS:
        value = mapped.get(key)
        if isinstance(value, Decimal):
            mapped[key] = float(value)

    for sn_key in (
        "cobrar_juros",
        "pagamento_posterior",
        "servico_gratuito",
        "pagamento_diferido",
        "titulo_antigo",
        "importar",
        "protestado",
        "apresentante_permitido",
        "cedente_permitido",
        "credor_permitido",
        "anuencia",
    ):
        if sn_key in mapped:
            mapped[sn_key] = normalize_sim_nao_from_db(mapped.get(sn_key))

    if "tipo_aceite" in mapped:
        raw_aceite = mapped.get("tipo_aceite")
        if raw_aceite is None or not str(raw_aceite).strip():
            mapped["tipo_aceite"] = None
        else:
            mapped["tipo_aceite"] = normalize_tipo_aceite(raw_aceite)
    if "tipo_endosso" in mapped:
        raw_endosso = mapped.get("tipo_endosso")
        if raw_endosso is None or not str(raw_endosso).strip():
            mapped["tipo_endosso"] = None
        else:
            mapped["tipo_endosso"] = normalize_tipo_endosso(raw_endosso)
    if "status_importacao" in mapped:
        raw_status = mapped.get("status_importacao")
        if raw_status is None or not str(raw_status).strip():
            mapped["status_importacao"] = None
        else:
            mapped["status_importacao"] = normalize_status_importacao(raw_status)

    mapped["selecao_status"] = normalize_selecao_status_from_db(mapped.get("selecao_status"))

    for text_key in (
        "numero_titulo",
        "nosso_numero",
        "numero_titulo_banco",
        "observacoes",
        "prazo",
        "protesto_artigo_9",
    ):
        if text_key in mapped:
            mapped[text_key] = _normalize_string_field(mapped.get(text_key))

    ocorrencia = mapped.pop("ocorrencia", None)
    if isinstance(ocorrencia, Mapping):
        occ = normalize_row_keys(ocorrencia) or {}
        oid = occ.get("ocorrencias_id")
        if isinstance(oid, Decimal):
            occ["ocorrencias_id"] = int(oid)
        mapped["ocorrencia"] = occ

    ocorrencia_andamento = mapped.pop("ocorrencia_andamento", None)
    if isinstance(ocorrencia_andamento, Mapping):
        oa = normalize_row_keys(ocorrencia_andamento) or {}
        oaid = oa.get("ocorrencia_andamento_id")
        if isinstance(oaid, Decimal):
            oa["ocorrencia_andamento_id"] = int(oaid)
        codigo = oa.get("codigo")
        if codigo is not None:
            oa["codigo"] = str(codigo).strip().upper() or None
        mapped["ocorrencia_andamento"] = oa

    pessoa_vinculos = mapped.pop("pessoa_vinculos", None)
    if isinstance(pessoa_vinculos, list):
        mapped["pessoa_vinculos"] = [
            _map_pessoa_vinculo_item(item) for item in pessoa_vinculos if item is not None
        ]

    andamentos = mapped.pop("andamentos", None)
    if isinstance(andamentos, list):
        mapped["andamentos"] = [
            _map_andamento_item(item) for item in andamentos if item is not None
        ]

    return mapped


def map_titulo_index_row(row: Optional[Mapping[str, Any]]) -> Optional[dict[str, Any]]:
    from database.orm_firebird import normalize_row_keys

    mapped = normalize_row_keys(row)
    if mapped is None:
        return None

    titulo_id = mapped.get("titulo_id")
    if isinstance(titulo_id, Decimal):
        titulo_id = int(titulo_id)

    especie_id = mapped.get("especie_id")
    if isinstance(especie_id, Decimal):
        especie_id = int(especie_id)

    ocorrencia_id = mapped.get("ocorrencia_id")
    if isinstance(ocorrencia_id, Decimal):
        ocorrencia_id = int(ocorrencia_id)

    banco_id = mapped.get("banco_id")
    if isinstance(banco_id, Decimal):
        banco_id = int(banco_id)

    numero_apontamento = mapped.get("numero_apontamento")
    if isinstance(numero_apontamento, Decimal):
        numero_apontamento = float(numero_apontamento)

    valor_titulo = mapped.get("valor_titulo")
    if isinstance(valor_titulo, Decimal):
        valor_titulo = float(valor_titulo)

    qtd = mapped.get("quantidade_pessoas_vinculadas") or mapped.get("qtd_pessoas_vinculadas")
    if isinstance(qtd, Decimal):
        qtd = int(qtd)

    especie_sigla = mapped.get("especie_sigla")
    if especie_sigla is not None:
        especie_sigla = str(especie_sigla).strip() or None

    especie_descricao = mapped.get("especie_descricao")
    if especie_descricao is not None:
        especie_descricao = str(especie_descricao).strip() or None

    ocorrencia_descricao = mapped.get("ocorrencia_descricao")
    if ocorrencia_descricao is not None:
        ocorrencia_descricao = str(ocorrencia_descricao).strip() or None

    banco_descricao = mapped.get("banco_descricao")
    if banco_descricao is not None:
        banco_descricao = str(banco_descricao).strip() or None

    result: dict[str, Any] = {
        "titulo_id": titulo_id,
        "numero_titulo": _normalize_string_field(mapped.get("numero_titulo")),
        "nosso_numero": _normalize_string_field(mapped.get("nosso_numero")),
        "numero_apontamento": numero_apontamento,
        "especie_id": especie_id,
        "valor_titulo": valor_titulo,
        "ocorrencia_id": ocorrencia_id,
        "banco_id": banco_id,
        "quantidade_pessoas_vinculadas": int(qtd or 0),
        "apresentante_nome": _normalize_string_field(
            mapped.get("apresentante_nome")
        ),
        "apresentante_cpfcnpj": _normalize_string_field(
            mapped.get("apresentante_cpfcnpj")
        ),
    }

    if especie_id is not None or especie_sigla or especie_descricao:
        result["especie"] = {
            "especie_id": especie_id,
            "especie": especie_sigla,
            "descricao": especie_descricao,
        }
    else:
        result["especie"] = None

    if ocorrencia_id is not None or ocorrencia_descricao:
        result["ocorrencia"] = {
            "ocorrencias_id": ocorrencia_id,
            "descricao": ocorrencia_descricao,
        }
    else:
        result["ocorrencia"] = None

    if banco_id is not None or banco_descricao:
        result["banco"] = {
            "banco_id": banco_id,
            "descricao": banco_descricao,
        }
    else:
        result["banco"] = None

    return result


def _map_pessoa_vinculo_item(row: Mapping[str, Any]) -> dict[str, Any]:
    from database.orm_firebird import normalize_row_keys

    mapped = normalize_row_keys(row) or {}
    for key in ("pessoa_vinculo_id", "titulo_id", "pessoa_id", "ocorrencia_id"):
        value = mapped.get(key)
        if isinstance(value, Decimal):
            mapped[key] = int(value)
    tipo = mapped.get("tipo_vinculo")
    if tipo is not None:
        mapped["tipo_vinculo"] = str(tipo).strip().upper() or None
    pessoa = mapped.pop("pessoa", None)
    if isinstance(pessoa, Mapping):
        p = normalize_row_keys(pessoa) or {}
        pid = p.get("pessoa_id")
        if isinstance(pid, Decimal):
            p["pessoa_id"] = int(pid)
        mapped["pessoa"] = p
    return mapped


def _map_andamento_item(row: Mapping[str, Any]) -> dict[str, Any]:
    from database.orm_firebird import normalize_row_keys

    mapped = normalize_row_keys(row) or {}
    for key in ("andamento_id", "titulo_id", "ocorrencia_andamento_id", "usuario_id"):
        value = mapped.get(key)
        if isinstance(value, Decimal):
            mapped[key] = int(value)
    oa = mapped.pop("ocorrencia_andamento", None)
    if isinstance(oa, Mapping):
        nested = normalize_row_keys(oa) or {}
        oaid = nested.get("ocorrencia_andamento_id")
        if isinstance(oaid, Decimal):
            nested["ocorrencia_andamento_id"] = int(oaid)
        mapped["ocorrencia_andamento"] = nested
    return mapped


def _map_selo_vinculado_item(row: Mapping[str, Any]) -> dict[str, Any]:
    """Linha do UNION G_SELO_LIVRO + G_SELO_LIVRO_ANTIGO → PTituloSeloVinculadoItem."""
    from database.orm_firebird import normalize_row_keys

    mapped = normalize_row_keys(row) or {}

    def _to_int(value: Any) -> Optional[int]:
        if value is None:
            return None
        if isinstance(value, Decimal):
            return int(value)
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            return int(value)
        if isinstance(value, str) and value.strip().isdigit():
            return int(value.strip())
        return None

    def _to_float(value: Any) -> Optional[float]:
        if value is None:
            return None
        if isinstance(value, Decimal):
            return float(value)
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            return float(value)
        return None

    data_val = mapped.get("data")
    if isinstance(data_val, datetime):
        data_out: Any = data_val.isoformat()
    else:
        data_out = data_val

    tipo_ato = mapped.get("tipo_ato")
    if isinstance(tipo_ato, Decimal):
        tipo_ato = int(tipo_ato)
    elif tipo_ato is not None and not isinstance(tipo_ato, (int, str)):
        try:
            tipo_ato = int(tipo_ato)
        except (TypeError, ValueError):
            tipo_ato = str(tipo_ato).strip() or None

    return {
        "nota_fiscal": mapped.get("nota_fiscal"),
        "campo_id": _to_int(mapped.get("campo_id")),
        "selo_agrupador": mapped.get("numero_agrupador"),
        "sigla": mapped.get("sigla"),
        "numero": _to_int(mapped.get("numero")),
        "tipo_ato": tipo_ato,
        "codigo_ato": tipo_ato,
        "descricao_completa": mapped.get("descricao_completa"),
        "nome_completo": mapped.get("nome_completo"),
        "data": data_out,
        "data_hora_utilizacao": data_out,
        "descricao": mapped.get("descricao"),
        "descricao_ato": mapped.get("descricao"),
        "valor_total": _to_float(mapped.get("valor_total")),
        "valor_emolumento": _to_float(mapped.get("valor_emolumento")),
        "valor_taxa_judiciaria": _to_float(mapped.get("valor_taxa_judiciaria")),
        "valor_fundesp": _to_float(mapped.get("valor_fundesp")),
        "selo_livro_id": _to_int(mapped.get("selo_livro_id")),
    }
