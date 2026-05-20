from numbers import Number

from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime

# ----------------------------------------------------
# Schema base - representa a tabela T_ATO
# ----------------------------------------------------
class TAtoSchema(BaseModel):
    ato_id: Optional[Decimal] = None
    ato_tipo_id: Optional[Decimal] = None
    escrevente_ato_id: Optional[Decimal] = None
    escrevente_assina_id: Optional[Decimal] = None
    livro_andamento_id: Optional[Decimal] = None

    data_abertura: Optional[datetime] = None
    data_lavratura: Optional[datetime] = None
    usuario_id: Optional[Decimal] = None
    protocolo: Optional[Decimal] = None
    alienacao_data: Optional[datetime] = None
    qualificacao_imovel_id: Optional[Decimal] = None

    folha_inicial: Optional[Decimal] = None
    folha_final: Optional[Decimal] = None
    folha_total: Optional[Decimal] = None
    alienacao_forma: Optional[Decimal] = None

    grs_numero: Optional[str] = None

    texto: Optional[bytes] = None
    texto_finalizacao: Optional[bytes] = None

    natureza_id: Optional[Decimal] = None
    valor_pagamento: Optional[Decimal] = None
    situacao_ato: Optional[str] = None

    texto_imovel_geral: Optional[bytes] = None
    texto_assinatura: Optional[bytes] = None

    cancelado_data: Optional[datetime] = None
    cancelado_motivo: Optional[str] = None
    cancelado_observacao: Optional[str] = None
    cancelado_usuario_id: Optional[Decimal] = None
    data_cancelamento: Optional[datetime] = None

    alienacao_datalavratura: Optional[str] = None
    ato_antigo: Optional[str] = None
    folha_letra: Optional[str] = None
    qtd_imovel: Optional[Decimal] = None
    minuta_protegida: Optional[str] = None
    havido_marcacao_id: Optional[Decimal] = None
    observacao: Optional[str] = None

    selo_livro_id: Optional[Decimal] = None
    usar_tabela_auxiliar: Optional[str] = None
    ato_antigo_ocorrencia: Optional[str] = None
    fonte_tamanho: Optional[Decimal] = None
    selo_recuo: Optional[Decimal] = None
    ato_antigo_protocolo: Optional[Decimal] = None

    cadastrar_imovel: Optional[str] = None

    filho_maior_qtd: Optional[Decimal] = None
    filho_maior_descricao: Optional[bytes] = None
    filho_menor_qtd: Optional[Decimal] = None
    filho_menor_descricao: Optional[bytes] = None

    casamento_data: Optional[datetime] = None
    casamento_tb_regime_id: Optional[Decimal] = None

    resp_filhos_maiores: Optional[str] = None
    resp_filhos_menores: Optional[str] = None

    censec_naturezalitigio_id: Optional[Decimal] = None
    censec_acordo: Optional[str] = None

    nlote: Optional[Decimal] = None
    especie_pagamento: Optional[str] = None
    fora_cartorio: Optional[str] = None
    nfse_id: Optional[Decimal] = None
    acao: Optional[Decimal] = None

    data_protocolo: Optional[datetime] = None
    frente_verso: Optional[str] = None
    lavratura_online: Optional[str] = None
    data_prevista_entrega: Optional[datetime] = None
    usuario_id_lavratura: Optional[Decimal] = None

    ativo: Optional[str] = None
    convalidacao: Optional[str] = None
    lado_folha_fim: Optional[str] = None
    ato_oneroso: Optional[str] = None
    mne: Optional[str] = None
    eh_restrito: Optional[str] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para localizar um registro pelo ID (GET /{id})
# ----------------------------------------------------
class TAtoIdSchema(BaseModel):
    ato_id: Decimal
    """Auditoria / histórico (JWT) — não obrigatório em todas as rotas."""
    usuario_id: Optional[Decimal] = None

    class Config:
        from_attributes = True


class TAtoAtoAnteriorSchema(BaseModel):
    ato_anterior_origem: Optional[int] = None
    ato_anterior_livro: Optional[str] = None
    ato_anterior_finicial: Optional[str] = None
    ato_anterior_tb_cartorio_id: Optional[int] = None
    ato_anterior_outorgante: Optional[str] = None
    ato_anterior_observacao: Optional[str] = None
    ato_anterior_ato_id: Optional[int] = None
    ato_anterior_data: Optional[str] = None
    ato_anterior_anotacao_adicional: Optional[bytes] = None
    ato_anterior_ato_tipo_id: Optional[int] = None
    ato_anterior_valor_documento: Optional[int] = None

    class Config:
        from_attributes = True


class TAtoAnteriorUpdateSchema(BaseModel):
    ato_id: Optional[int] = None
    ato_anterior_origem: Optional[int] = None
    ato_anterior_livro: Optional[str] = None
    ato_anterior_finicial: Optional[str] = None
    ato_anterior_tb_cartorio_id: Optional[int] = None
    ato_anterior_outorgante: Optional[str] = None
    ato_anterior_observacao: Optional[str] = None
    ato_anterior_ato_id: Optional[int] = None
    ato_anterior_data: Optional[str] = None
    ato_anterior_anotacao_adicional: Optional[bytes] = None
    ato_anterior_ato_tipo_id: Optional[int] = None
    ato_anterior_valor_documento: Optional[int] = None

    class Config:
        from_attributes = True


class TAtoAnteriorClearSchema(BaseModel):
    ato_id: Decimal
    usuario_id: Optional[Decimal] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para localizar um registro pelo ID (GET /{id})
# ----------------------------------------------------
class TAtoLavraturaSchema(BaseModel):
    ato_id: Decimal
    usuario_id: Optional[Decimal] = None
    situacao_ato: Optional[Decimal] = None
    folha_inicial: Optional[Decimal] = None
    folha_final: Optional[Decimal] = None
    folha_total: Optional[Decimal] = None
    livro_andamento_id: Optional[Decimal] = None
    selo_livro_id: Optional[Decimal] = None

    class Config:
        from_attributes = True


class TAtoClearTextoSchema(BaseModel):
    ato_id: Decimal
    usuario_id: Optional[Decimal] = None

    class Config:
        from_attributes = True


class TAtoClearTextoAssinaturaSchema(BaseModel):
    ato_id: Decimal
    tipo_assinatura: int
    usuario_id: Optional[Decimal] = None
    coluna: Optional[str] = None

    class Config:
        from_attributes = True


class TAtoClearTextoFinalizacaoSchema(BaseModel):
    ato_id: Decimal
    tipo_finalizacao: int
    usuario_id: Optional[Decimal] = None
    coluna: Optional[str] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para localizar um registro pelo ID (GET /{id})
# ----------------------------------------------------
class TAtoTextoVisualizarSchema(BaseModel):
    ato_id: Decimal
    tipo_visualizacao: Decimal
    coluna: Optional[str] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para localizar um registro pelo ID (GET /{id})
# ----------------------------------------------------
class TAtoTextoFinalizacao(BaseModel):

    ato_id: Decimal
    tipo_finalizacao: Decimal
    coluna: Optional[str] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para buscar texto de assinatura por ato e tipo
# ----------------------------------------------------
class TAtoTextoAssinatura(BaseModel):

    ato_id: Decimal
    tipo_assinatura: Decimal
    coluna: Optional[str] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para localizar um registro pelo ID (GET /{id})
# ----------------------------------------------------
class TAtoTextoFinalizacaoUpdateSchema(BaseModel):

    ato_id: Decimal
    tipo_finalizacao: Decimal
    coluna: Optional[str] = None
    texto: Optional[bytes] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para atualizar texto de assinatura por ato e tipo
# ----------------------------------------------------
class TAtoTextoAssinaturaUpdateSchema(BaseModel):

    ato_id: Optional[Decimal] = None
    tipo_assinatura: Optional[Decimal] = None
    coluna: Optional[str] = None
    texto: Optional[bytes] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para criação (POST)
# ----------------------------------------------------
class TAtoSaveSchema(TAtoSchema):
    situacao_ato: Optional[str] = "1"


# ----------------------------------------------------
# Schema para atualização (PUT)
# ----------------------------------------------------
class TAtoUpdateSchema(TAtoSchema):
    pass


# ----------------------------------------------------
# Schema para atualização (PUT)
# ----------------------------------------------------
class TAtoSaveMinuta(BaseModel):
    ato_id: Optional[int] = None
    minuta_id: int
    texto: Optional[bytes] = None
    pass


# ----------------------------------------------------
# Schema para atualização (PUT)
# ----------------------------------------------------
class TAtoUpdateTextoSchema(BaseModel):
    ato_id: Optional[int] = None
    texto: Optional[bytes] = None
    pass


class TAtoProtocolarUpdateSchema(BaseModel):
    ato_id: Decimal
    protocolo: Decimal

    class Config:
        from_attributes = True
