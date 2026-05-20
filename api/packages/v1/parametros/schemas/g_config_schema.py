from typing import Optional
from pydantic import BaseModel, ConfigDict


class GConfigSchema(BaseModel):
    config_id: Optional[float] = None
    config_grupo_id: Optional[float] = None
    config_padrao_id: Optional[float] = None
    secao: Optional[str] = None
    nome: Optional[str] = None
    valor: Optional[str] = None
    descricao: Optional[str] = None
    texto: Optional[bytes] = None
    terminal: Optional[str] = None
    tipo_valor: Optional[str] = None
    atualizado: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class GConfigResponseSchema(GConfigSchema):
    model_config = ConfigDict(from_attributes=True)

class GConfigIdSchema(BaseModel):
    config_id: float
    model_config = ConfigDict(from_attributes=True)


class GConfigSaveSchema(GConfigSchema):
    config_id: Optional[float] = None
    model_config = ConfigDict(from_attributes=True)

class GConfigUpdateSchema(GConfigSchema):
    model_config = ConfigDict(from_attributes=True)


class GConfigIndexFilterSchema(BaseModel):
    sistema_id: float
    secao: str
    descricao: str
    model_config = ConfigDict(from_attributes=True)


class GConfigShowByBreadcumbSchema(BaseModel):
    nome: str = None
    secao: str = None
    grupo_descricao: str = None
    sistema_id: float = None
    model_config = ConfigDict(from_attributes=True)


class GConfigNomeSchema(BaseModel):
    nome: str = None
    sistema_id: float = None
    model_config = ConfigDict(from_attributes=True)
