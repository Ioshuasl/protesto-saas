from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime


# ----------------------------------------------------
# Schema base - representa a tabela T_ATO_ANDAMENTO
# ----------------------------------------------------
class TAtoAndamentoSchema(BaseModel):
    ato_andamento_id: Optional[Decimal] = None
    tb_andamentoservico_id: Optional[Decimal] = None
    ato_id: Optional[Decimal] = None
    usuario_id: Optional[Decimal] = None
    data_andamento: Optional[datetime] = None
    observacao: Optional[bytes] = None
    complemento: Optional[str] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para localizar um registro pelo ID (GET /{id})
# ----------------------------------------------------
class TAtoAndamentoIndexSchema(BaseModel):
    ato_id: Decimal

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para localizar um registro pelo ID (GET /{id})
# ----------------------------------------------------
class TAtoAndamentoIdSchema(BaseModel):
    ato_andamento_id: Decimal

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para criação (POST)
# ----------------------------------------------------
class TAtoAndamentoSaveSchema(TAtoAndamentoSchema):
    pass


# ----------------------------------------------------
# Schema para atualização (PUT)
# ----------------------------------------------------
class TAtoAndamentoUpdateSchema(TAtoAndamentoSchema):
    pass
