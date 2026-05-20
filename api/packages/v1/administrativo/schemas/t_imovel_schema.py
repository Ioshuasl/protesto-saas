from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# ----------------------------------------------------
# Schema base
# ----------------------------------------------------
class TImovelSchema(BaseModel):
    imovel_id: Optional[int] = None
    tipo_classe: Optional[int] = None
    tipo_registro: Optional[str] = None
    data_registro: Optional[datetime] = None
    numero: Optional[float] = None
    numero_letra: Optional[str] = None
    cidade: Optional[str] = None
    cep: Optional[float] = None
    uf: Optional[str] = None
    tb_bairro_id: Optional[int] = None
    cartorio: Optional[int] = None
    livro: Optional[str] = None
    cns: Optional[float] = None

    class Config:
        from_attributes = True

# ----------------------------------------------------
# Schema base
# ----------------------------------------------------
class TImovelIndexSchema(BaseModel):
    tipo_classe: int

    class Config:
        from_attributes = True

# ----------------------------------------------------
# Schema para localizar um IMÓVEL pelo ID (GET)
# ----------------------------------------------------
class TImovelIdSchema(BaseModel):
    imovel_id: int

    class Config:
        from_attributes = True

# ----------------------------------------------------
# Schema para criação de novo IMÓVEL (POST)
# ----------------------------------------------------
class TImovelSaveSchema(BaseModel):
    imovel_id: Optional[int] = None
    tipo_classe: Optional[int] = None
    tipo_registro: Optional[str] = None
    data_registro: Optional[datetime] = None
    numero: Optional[float] = None
    numero_letra: Optional[str] = None
    cidade: Optional[str] = None
    cep: Optional[float] = None
    uf: Optional[str] = None
    tb_bairro_id: Optional[int] = None
    cartorio: Optional[int] = None
    livro: Optional[str] = None
    cns: Optional[float] = None

    class Config:
        from_attributes = True

# ----------------------------------------------------
# Schema para atualização de IMÓVEL (PUT)
# ----------------------------------------------------
class TImovelUpdateSchema(BaseModel):
    imovel_id: int
    tipo_classe: Optional[int] = None
    tipo_registro: Optional[str] = None
    data_registro: Optional[datetime] = None
    numero: Optional[float] = None
    numero_letra: Optional[str] = None
    cidade: Optional[str] = None
    cep: Optional[float] = None
    uf: Optional[str] = None
    tb_bairro_id: Optional[int] = None
    cartorio: Optional[int] = None
    livro: Optional[str] = None
    cns: Optional[float] = None

    class Config:
        from_attributes = True
