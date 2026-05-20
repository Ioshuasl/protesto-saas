from datetime import date
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel


class CaixaItemSchema(BaseModel):
    especie_pagamento: Optional[str] = None
    caixa_item_id: Optional[int] = None
    caixa_servico_id: Optional[int] = None
    usuario_servico_id: Optional[int] = None
    usuario_caixa_id: Optional[int] = None
    chave_servico: Optional[Decimal] = None
    descricao: Optional[str] = None
    data_pagamento: Optional[date] = None
    situacao: Optional[int] = None
    tipo_documento: Optional[str] = None
    tipo_transacao: Optional[str] = None
    valor_servico: Optional[float] = None
    valor_pago: Optional[Decimal] = None
    observacao: Optional[Decimal] = None
    caixa_cheque_id: Optional[int] = None
    hora_pagamento: Optional[str] = None
    caixa_id: Optional[int] = None
    recibo_id: Optional[int] = None
    tipo_servico: Optional[str] = None
    qtd: Optional[int] = None
    apresentante: Optional[str] = None
    mensalista_id: Optional[int] = None
    quitado_caixa_id: Optional[int] = None
    registrado: Optional[int] = None
    emolumento: Optional[Decimal] = None
    taxa_judiciaria: Optional[Decimal] = None
    fundesp: Optional[float] = None
    desconto: Optional[float] = None
    valor_documento: Optional[float] = None
    outra_taxa1: Optional[float] = None
    chave_servico_sec: Optional[str] = None
    emolumento_item_id: Optional[Decimal] = None
    caixa_registroselo_id: Optional[int] = None
    fundo_ri: Optional[float] = None
    valor_recibo: Optional[float] = None
    boleto_pdf: Optional[str] = None  # ou `bytes` se for binário
    boleto_vencimento: Optional[date] = None
    iss: Optional[float] = None
    nlote: Optional[int] = None
    tabela: Optional[str] = None
    campo_id: Optional[int] = None
    boleto_id: Optional[int] = None
    valor_adicional: Optional[float] = None
    pix_id: Optional[int] = None
    cpfcnpj_apresentante: Optional[str] = None
    origem_pagamento: Optional[str] = None
    conta_corrente: Optional[str] = None
    valor_fundo_selo: Optional[Decimal] = None
    vrcext: Optional[Decimal] = None
    fornecedor_id: Optional[int] = None
    data_competencia: Optional[date] = None
    data_vencimento: Optional[date] = None
    protocolo_onr: Optional[str] = None
    data_recebido_onr: Optional[date] = None
    valor_taxa: Optional[Decimal] = None
    cpf_cnpj_pagador: Optional[str] = None
    nome_pagador: Optional[str] = None
    despesa_diario_auxiliar: Optional[Decimal] = None
    numero_boleto_onr: Optional[str] = None
    chave_servico_onr: Optional[str] = None
    tipo_baixa: Optional[str] = None
    xml_compensacao_onr_id: Optional[int] = None
    data_devolucao: Optional[date] = None

    class Config:
        from_attributes = True


class IntervaloDatas(BaseModel):
    date_start: Optional[str] = None
    date_end: Optional[str] = None


class CaixaItemSearchSchema(BaseModel):
    data_pagamento: Optional[IntervaloDatas] = None
