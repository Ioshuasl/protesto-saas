from typing import Optional

from pydantic import BaseModel, field_validator

from actions.validations.text import Text


# ----------------------------------------------------
# Schema base
# ----------------------------------------------------
class TMinutaSchema(BaseModel):
    minuta_id: Optional[int] = None
    ato_tipo_id: Optional[int] = None
    natureza_id: Optional[int] = None
    descricao: Optional[str] = None
    texto: Optional[bytes] = None
    protegida: Optional[str] = None
    situacao: Optional[str] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para localizar uma MINUTA especifica pelo ID (GET)
# ----------------------------------------------------
class TMinutaIdSchema(BaseModel):
    minuta_id: Optional[int] = None


# ----------------------------------------------------
# Schema para localizar uma MINUTA especifica pela descricao (GET)
# ----------------------------------------------------
class TMinutaDescricaoSchema(BaseModel):
    descricao: Optional[str] = None


# ----------------------------------------------------
# Schema para criacao de nova MINUTA (POST)
# ----------------------------------------------------
class TMinutaSaveSchema(BaseModel):
    minuta_id: Optional[int] = None
    ato_tipo_id: Optional[int] = None
    natureza_id: Optional[int] = None
    descricao: Optional[str] = None
    texto: Optional[bytes] = None
    protegida: Optional[str] = None
    situacao: Optional[str] = None

    @field_validator("descricao", "protegida", "situacao")
    def sanitize_fields(cls, v: Optional[str]) -> Optional[str]:
        if isinstance(v, str) and v:
            return Text.sanitize_input(v)
        return v

    @field_validator("texto")
    def validate_blob(cls, v: Optional[bytes]) -> Optional[bytes]:
        if v is not None and not isinstance(v, bytes):
            raise ValueError("O campo de texto deve ser do tipo bytes.")
        return v


# ----------------------------------------------------
# Schema para atualizar MINUTA (PUT)
# ----------------------------------------------------
class TMinutaUpdateSchema(BaseModel):
    ato_tipo_id: Optional[int] = None
    natureza_id: Optional[int] = None
    descricao: Optional[str] = None
    texto: Optional[bytes] = None
    protegida: Optional[str] = None
    situacao: Optional[str] = None

    @field_validator("descricao", "protegida", "situacao")
    def sanitize_fields(cls, v: Optional[str]) -> Optional[str]:
        if isinstance(v, str) and v:
            return Text.sanitize_input(v)
        return v

    @field_validator("texto")
    def validate_blob(cls, v: Optional[bytes]) -> Optional[bytes]:
        if v is not None and not isinstance(v, bytes):
            raise ValueError("O campo de texto deve ser do tipo bytes.")
        return v


# ----------------------------------------------------
# Schema para atualizar MINUTA (PUT)
# ----------------------------------------------------
class TMinutaUpdateTextoSchema(BaseModel):
    texto: Optional[bytes] = None
    minuta_id: Optional[int] = None