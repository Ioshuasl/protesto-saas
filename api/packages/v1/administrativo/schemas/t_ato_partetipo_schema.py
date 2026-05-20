from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Optional


# ----------------------------------------------------
# Schema base
# ----------------------------------------------------
class TAtoParteTipoSchema(BaseModel):
    ato_partetipo_id: Decimal = Field(..., description="Identificador único da parte do ato")
    descricao: Optional[str] = Field(None, max_length=60)
    tipo_parte: Optional[Decimal] = None
    auto_qualifica: Optional[str] = Field(None, max_length=1)
    declara_doi: Optional[str] = Field(None, max_length=1)
    possui_documento_ext: Optional[str] = Field(None, max_length=1)
    situacao: Optional[str] = Field(None, max_length=1)
    texto: Optional[bytes] = None
    censec_qualidade_id: Optional[Decimal] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para indexação
# ----------------------------------------------------
class TAtoParteTipoIndexSchema(BaseModel):
    ato_partetipo_id: int

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para busca por ID (GET)
# ----------------------------------------------------
class TAtoParteTipoIdSchema(BaseModel):
    ato_partetipo_id: int

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para criação (POST)
# ----------------------------------------------------
class TAtoParteTipoSaveSchema(BaseModel):
    ato_partetipo_id: Optional[int] = None
    descricao: Optional[str] = Field(None, max_length=60)
    tipo_parte: Optional[Decimal] = None
    auto_qualifica: Optional[str] = Field(None, max_length=1)
    declara_doi: Optional[str] = Field(None, max_length=1)
    possui_documento_ext: Optional[str] = Field(None, max_length=1)
    situacao: Optional[str] = Field(None, max_length=1)
    texto: Optional[bytes] = None
    censec_qualidade_id: Optional[Decimal] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para atualização (PUT)
# ----------------------------------------------------
class TAtoParteTipoUpdateSchema(BaseModel):
    ato_partetipo_id: Optional[int] = None
    descricao: Optional[str] = Field(None, max_length=60)
    tipo_parte: Optional[Decimal] = None
    auto_qualifica: Optional[str] = Field(None, max_length=1)
    declara_doi: Optional[str] = Field(None, max_length=1)
    possui_documento_ext: Optional[str] = Field(None, max_length=1)
    situacao: Optional[str] = Field(None, max_length=1)
    texto: Optional[bytes] = None
    censec_qualidade_id: Optional[Decimal] = None

    class Config:
        from_attributes = True