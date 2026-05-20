from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# ----------------------------------------------------
# Schema base - representa a tabela G_EMOLUMENTO_PERIODO
# ----------------------------------------------------
class GEmolumentoPeriodoSchema(BaseModel):
    emolumento_periodo_id: Optional[float] = None
    descricao: Optional[str] = None
    situacao: Optional[str] = None
    data_inicial: Optional[datetime] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para localizar um registro pelo ID (GET /{id})
# ----------------------------------------------------
class GEmolumentoPeriodoIdSchema(BaseModel):
    emolumento_periodo_id: float

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para criação (POST)
# ----------------------------------------------------
class GEmolumentoPeriodoSaveSchema(BaseModel):
    emolumento_periodo_id: Optional[float] = None
    descricao: Optional[str] = None
    situacao: Optional[str] = None
    data_inicial: Optional[datetime] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para atualização (PUT)
# ----------------------------------------------------
class GEmolumentoPeriodoUpdateSchema(BaseModel):
    emolumento_periodo_id: Optional[float] = None
    descricao: Optional[str] = None
    situacao: Optional[str] = None
    data_inicial: Optional[datetime] = None

    class Config:
        from_attributes = True