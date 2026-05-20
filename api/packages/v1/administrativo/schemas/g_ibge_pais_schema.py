from pydantic import BaseModel
from typing import Optional


class GIbgePaisSchema(BaseModel):
    ibge_pais_id: Optional[str] = None
    descricao: Optional[str] = None
    cod_pais: Optional[str] = None

    class Config:
        from_attributes = True


class GIbgePaisIdSchema(BaseModel):
    ibge_pais_id: str

    class Config:
        from_attributes = True


class GIbgePaisSaveSchema(BaseModel):
    ibge_pais_id: Optional[str] = None
    descricao: Optional[str] = None
    cod_pais: Optional[str] = None

    class Config:
        from_attributes = True


class GIbgePaisUpdateSchema(BaseModel):
    ibge_pais_id: Optional[str] = None
    descricao: Optional[str] = None
    cod_pais: Optional[str] = None

    class Config:
        from_attributes = True
