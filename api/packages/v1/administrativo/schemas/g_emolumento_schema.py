from decimal import Decimal
from pydantic import BaseModel
from typing import Optional


class GEmolumentoIndexSchema(BaseModel):
    class Config:
        extra = "allow"


# ----------------------------------------------------
# Schema base - representa a tabela G_EMOLUMENTO
# ----------------------------------------------------
class GEmolumentoSchema(BaseModel):
    emolumento_id: Optional[float] = None
    descricao: Optional[str] = None
    tipo: Optional[str] = None
    sistema_id: Optional[float] = None
    selo_grupo_id: Optional[float] = None
    reg_averb: Optional[str] = None
    pre_definido: Optional[str] = None
    situacao: Optional[str] = None
    situacao_ri: Optional[str] = None
    com_reducao: Optional[str] = None
    motivo_reducao: Optional[str] = None
    valor_maximo_certidao: Optional[float] = None
    tipo_objetivo: Optional[str] = None
    modelo_tag: Optional[str] = None
    codigo_nota_id: Optional[float] = None
    convenio_codhab: Optional[str] = None
    item_df: Optional[str] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para localizar um registro pelo ID (GET /{id})
# ----------------------------------------------------
class GEmolumentoIdSchema(BaseModel):
    emolumento_id: float

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para localizar um registro pelo ID (GET /{id})
# ----------------------------------------------------
class GEmolumentoSistemaIdSchema(BaseModel):
    sistema_id: Decimal

    class Config:
        from_attributes = True
        extra = "allow"


# ----------------------------------------------------
# Schema para criação (POST)
# ----------------------------------------------------
class GEmolumentoSaveSchema(BaseModel):
    emolumento_id: Optional[float] = None
    descricao: Optional[str] = None
    tipo: Optional[str] = None
    sistema_id: Optional[float] = None
    selo_grupo_id: Optional[float] = None
    reg_averb: Optional[str] = None
    pre_definido: Optional[str] = None
    situacao: Optional[str] = None
    situacao_ri: Optional[str] = None
    com_reducao: Optional[str] = None
    motivo_reducao: Optional[str] = None
    valor_maximo_certidao: Optional[float] = None
    tipo_objetivo: Optional[str] = None
    modelo_tag: Optional[str] = None
    codigo_nota_id: Optional[float] = None
    convenio_codhab: Optional[str] = None
    item_df: Optional[str] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para atualização (PUT)
# ----------------------------------------------------
class GEmolumentoUpdateSchema(BaseModel):
    emolumento_id: Optional[float] = None
    descricao: Optional[str] = None
    tipo: Optional[str] = None
    sistema_id: Optional[float] = None
    selo_grupo_id: Optional[float] = None
    reg_averb: Optional[str] = None
    pre_definido: Optional[str] = None
    situacao: Optional[str] = None
    situacao_ri: Optional[str] = None
    com_reducao: Optional[str] = None
    motivo_reducao: Optional[str] = None
    valor_maximo_certidao: Optional[float] = None
    tipo_objetivo: Optional[str] = None
    modelo_tag: Optional[str] = None
    codigo_nota_id: Optional[float] = None
    convenio_codhab: Optional[str] = None
    item_df: Optional[str] = None

    class Config:
        from_attributes = True
