from pydantic import BaseModel
from typing import Optional
from decimal import Decimal


# ----------------------------------------------------
# Schema base - representa a tabela T_ATO_VINCULOVALOR
# ----------------------------------------------------
class TAtoVinculoValorSchema(BaseModel):
    ato_vinculovalor_id: Optional[Decimal] = None
    """Auditoria / histórico — verificar coluna na tabela antes de persistir."""
    usuario_id: Optional[Decimal] = None
    ato_id: Optional[Decimal] = None
    # Identificador do sistema (ex.: Tabelionato de Notas)
    sistema_id: Optional[Decimal] = None
    emolumento: Optional[Decimal] = None
    taxa_judiciaria: Optional[Decimal] = None
    emolumento_id: Optional[Decimal] = None
    fundesp: Optional[Decimal] = None
    valor_total: Optional[Decimal] = None
    emolumento_desconto: Optional[Decimal] = None
    natureza_titulo_id: Optional[Decimal] = None
    valor_documento: Optional[Decimal] = None
    quantidade: Optional[Decimal] = None
    tipo_cobranca: Optional[Decimal] = None
    item_padrao: Optional[str] = None
    valor_outra_taxa1: Optional[Decimal] = None
    item_complementar: Optional[str] = None
    item_manual: Optional[str] = None
    emolumento_corretor: Optional[Decimal] = None
    emolumento_item_id: Optional[Decimal] = None
    valor_adicional: Optional[Decimal] = None
    diferenca_situacao: Optional[str] = None
    diferenca_descricao: Optional[str] = None
    diferenca_tipo: Optional[str] = None
    valor_iss: Optional[Decimal] = None
    id_ato_isentado: Optional[Decimal] = None
    isento_emolumento_id: Optional[Decimal] = None
    motivo_isencao: Optional[str] = None
    ato_vinculoimovel_id: Optional[Decimal] = None
    nlote: Optional[Decimal] = None
    emol_principal: Optional[str] = None
    motivo_isencao_id: Optional[Decimal] = None
    valor_informacoes_centrais: Optional[Decimal] = None
    situacao_diferido: Optional[str] = None
    motivo_diferido: Optional[str] = None
    sigla_numero: Optional[str] = None
    valor_bens: Optional[Decimal] = None
    emolumento_acresce: Optional[Decimal] = None
    taxa_acresce: Optional[Decimal] = None
    funcivil_acresce: Optional[Decimal] = None
    cod_fator: Optional[Decimal] = None
    qtd_km: Optional[Decimal] = None
    valor_avaliacao: Optional[Decimal] = None
    distribuicao: Optional[Decimal] = None
    fundo_selo: Optional[Decimal] = None
    vrcext: Optional[Decimal] = None

    class Config:
        from_attributes = True


class TAtoVinculoValorIndexSchema(BaseModel):
    ato_id: Decimal

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para localizar um registro pelo ID (GET /{id})
# ----------------------------------------------------
class TAtoVinculoValorIdSchema(BaseModel):
    ato_vinculovalor_id: Decimal
    usuario_id: Optional[Decimal] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para criação (POST)
# ----------------------------------------------------
class TAtoVinculoValorSaveSchema(TAtoVinculoValorSchema):
    pass


# ----------------------------------------------------
# Schema para atualização (PUT)
# ----------------------------------------------------
class TAtoVinculoValorUpdateSchema(TAtoVinculoValorSchema):
    pass
