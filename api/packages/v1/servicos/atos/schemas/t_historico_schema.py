from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime


# ----------------------------------------------------
# Schema base - representa a tabela T_HISTORICO
# ----------------------------------------------------
class THistoricoSchema(BaseModel):
    historico_id: Optional[Decimal] = None
    hash: Optional[str] = None
    tabela: Optional[str] = None
    campo: Optional[str] = None
    operacao: Optional[str] = None
    new_value: Optional[bytes] = None
    usuario_id: Optional[Decimal] = None
    data: Optional[datetime] = None
    id: Optional[Decimal] = None
    observacao: Optional[str] = None
    data_registro: Optional[datetime] = None
    dados_complementares: Optional[bytes] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para listagem / indexação (GET)
# ----------------------------------------------------
class THistoricoIndexSchema(BaseModel):
    id: Optional[Decimal] = None
    tabela: Optional[str] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para localizar um registro pelo ID (GET /{id})
# ----------------------------------------------------
class THistoricoIdSchema(BaseModel):
    historico_id: Decimal

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para criação (POST)
# ----------------------------------------------------
class THistoricoHashSchema(BaseModel):
    hash_input: str
    hash: Optional[str] = None

    class Config:
        from_attributes = True


class THistoricoSaveSchema(THistoricoSchema):
    pass


# ----------------------------------------------------
# Schema para atualização (PUT)
# ----------------------------------------------------
class THistoricoUpdateSchema(THistoricoSchema):
    pass
