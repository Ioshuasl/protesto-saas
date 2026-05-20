from pydantic import BaseModel
from typing import Any, Optional
from decimal import Decimal
from datetime import datetime


class TServicoItemPedidoSchema(BaseModel):
    servico_itempedido_id: Optional[Decimal] = None
    servico_pedido_id: Optional[Decimal] = None
    servico_tipo_id: Optional[Decimal] = None
    valor: Optional[Decimal] = None
    qtd: Optional[Decimal] = None
    pessoa_id: Optional[Decimal] = None
    impressao_etiqueta: Optional[str] = None
    situacao: Optional[str] = None
    etiqueta_numero: Optional[Decimal] = None
    pessoa_auxiliar_id: Optional[Decimal] = None
    pessoa_sp_abono_rep: Optional[str] = None
    tipo_item: Optional[str] = None
    imprimir: Optional[str] = None
    observacao: Optional[str] = None
    impressao_direta: Optional[str] = None
    selo_livro_id: Optional[Decimal] = None
    emolumento: Optional[Decimal] = None
    fundesp: Optional[Decimal] = None
    taxa_judiciaria: Optional[Decimal] = None
    desconto: Optional[Decimal] = None
    desc_complementar: Optional[str] = None
    valor_manual: Optional[str] = None
    valor_documento: Optional[Decimal] = None
    outra_taxa1: Optional[Decimal] = None
    emolumento_item_id: Optional[Decimal] = None
    certidao_impressa: Optional[str] = None
    certidao_ato_id: Optional[Decimal] = None
    emolumento_id: Optional[Decimal] = None
    certidao_previsao: Optional[datetime] = None
    certidao_ato_antigo: Optional[str] = None
    certidao_data_emissao: Optional[datetime] = None
    certidao_texto: Optional[str] = None
    ato_antigo_tipo: Optional[str] = None
    valor_iss: Optional[Decimal] = None
    id_ato_isentado: Optional[Decimal] = None
    motivo_isencao: Optional[str] = None
    pessoas_etiquetas: Optional[Decimal] = None
    abonador: Optional[str] = None
    servico_cartao: Optional[str] = None
    valor_informacoes_centrais: Optional[Decimal] = None
    situacao_diferido: Optional[str] = None
    sigla_numero: Optional[str] = None
    motivo_diferido: Optional[str] = None
    nome_juridico: Optional[str] = None
    etiqueta_apenas_frente: Optional[str] = None
    indexacao_id: Optional[Decimal] = None
    certidao_data_lavratura: Optional[datetime] = None
    nfse_id: Optional[Decimal] = None
    qtd_pagina_certidao: Optional[Decimal] = None
    placa: Optional[str] = None
    dut: Optional[str] = None
    etiqueta_unica: Optional[str] = None
    fundo_abonador: Optional[str] = None
    instrumento_publico: Optional[str] = None
    data_lavratura_abono: Optional[datetime] = None
    valor_base_calculo: Optional[Decimal] = None
    valor_avaliacao: Optional[Decimal] = None
    ato_abonado: Optional[Decimal] = None
    transferencia_veiculo: Optional[str] = None
    usar_a4: Optional[str] = None
    cpf_abono_rep: Optional[str] = None
    vrcext: Optional[Decimal] = None
    valor_fundo_selo: Optional[Decimal] = None
    averbacao: Optional[str] = None
    usuario_id: Optional[int] = None
    cartao_data: Optional[str] = None
    cartao_numero: Optional[int] = None

    class Config:
        from_attributes = True


class TServicoItemIndexSchema(BaseModel):
    servico_pedido_id: Optional[Decimal] = None
    usuario_id: Optional[Decimal] = None

    class Config:
        from_attributes = True


class TServicoItemPedidoIdSchema(BaseModel):
    servico_itempedido_id: Optional[Decimal] = None

    class Config:
        from_attributes = True


class TServicoItemPedidoSituacaoSchema(BaseModel):
    servico_itempedido_id: Optional[Decimal] = None
    usuario_id: Optional[Decimal] = None

    class Config:
        from_attributes = True


class TServicoItemPedidoQuantidadeSchema(BaseModel):

    servico_itempedido_id: Optional[Decimal] = None
    qtd: Decimal = None
    usuario_id: Optional[Decimal] = None

    class Config:
        from_attributes = True


class TServicoItemPedidoSaveSituacaoSchema(BaseModel):

    servico_itempedido_id: int = None
    situacao: str = None

    class Config:
        from_attributes = True


class TServicoItemPedidoCertidaoSaveSchema(BaseModel):

    servico_itempedido_id: int = None
    data: object
    certidao_texto: Optional[bytes] = None

    class Config:
        from_attributes = True


class TServicoItemPedidoSaveSchema(TServicoItemPedidoSchema):

    class Config:
        from_attributes = True


class TServicoItemPedidoSaveSchema_(TServicoItemPedidoSchema):

    emolumento_id: Optional[Decimal] = None
    emolumento_item_id: Optional[Decimal] = None
    servico_tipo_id: Optional[Decimal] = None
    tipo_item: Optional[str] = None
    descricao: Optional[str] = None
    tabela: Optional[str] = None
    situacao: Optional[str] = None
    qtd: Optional[int] = None
    valor: Optional[Decimal] = None
    emolumento: Optional[Decimal] = None
    fundesp: Optional[Decimal] = None
    taxa_judiciaria: Optional[Decimal] = None
    valor_iss: Optional[Decimal] = None
    pessoa_id: Optional[Decimal] = None
    index: Optional[int] = None

    class Config:
        from_attributes = True


class TServicoItemPedidoCreateCertidaoSchema(BaseModel):

    servico_itempedido_id: int
    certidao_texto: Optional[Any] = None

    class Config:
        from_attributes = True


class TServicoItemPedidoUpdateSchema(TServicoItemPedidoSchema):

    class Config:
        from_attributes = True
