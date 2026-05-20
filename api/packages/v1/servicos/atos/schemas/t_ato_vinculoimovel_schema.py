from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime


# ----------------------------------------------------
# Schema base - representa a tabela T_ATO_VINCULOIMOVEL
# ----------------------------------------------------
class TAtoVinculoImovelSchema(BaseModel):
    ato_vinculoimovel_id: Optional[Decimal] = None
    """Auditoria / histórico — não existe coluna USUARIO_ID em T_ATO_VINCULOIMOVEL."""
    usuario_id: Optional[Decimal] = None
    ato_id: Optional[Decimal] = None
    registro_numero: Optional[str] = None
    imovel_unidade_id: Optional[Decimal] = None
    valor_avaliacao: Optional[Decimal] = None
    valor_alienacao: Optional[Decimal] = None
    valor_aliquota: Optional[Decimal] = None
    imovel_id: Optional[Decimal] = None
    valor_maior: Optional[Decimal] = None
    registro_data: Optional[datetime] = None
    tipo_ato_onr: Optional[Decimal] = None
    valortransmissao: Optional[Decimal] = None
    valorvenal: Optional[Decimal] = None
    valorfinanciamento: Optional[Decimal] = None
    valorleilao: Optional[Decimal] = None
    recursosproprios: Optional[Decimal] = None
    recursosfinanciado: Optional[Decimal] = None
    primeiraaquisicao: Optional[Decimal] = None
    observacoesgerais: Optional[str] = None
    descrever: Optional[str] = None
    valor_pago_data_ato: Optional[Decimal] = None
    permuta_bens: Optional[str] = None
    pagamento_em_dinheiro: Optional[str] = None
    valor_pago_em_dinheiro: Optional[Decimal] = None
    data_ultima_parcela: Optional[datetime] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para localizar um registro pelo ID (GET /{id})
# ----------------------------------------------------
class TAtoVinculoImovelIndexSchema(BaseModel):
    ato_id: Decimal

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para localizar um registro pelo ID (GET /{id})
# ----------------------------------------------------
class TAtoVinculoImovelIdSchema(BaseModel):
    ato_vinculoimovel_id: Decimal
    usuario_id: Optional[Decimal] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para criação (POST)
# ----------------------------------------------------
class TAtoVinculoImovelSaveSchema(TAtoVinculoImovelSchema):
    pass


# ----------------------------------------------------
# Schema para atualização (PUT)
# ----------------------------------------------------
class TAtoVinculoImovelUpdateSchema(TAtoVinculoImovelSchema):
    pass
