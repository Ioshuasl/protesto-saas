from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator

from actions.validations.text import Text

ESPECIE_MAX_LENGTH = 3


def normalize_especie(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    normalized = str(value).strip().upper()
    if not normalized:
        raise ValueError("A sigla (especie) é obrigatória.")
    if len(normalized) > ESPECIE_MAX_LENGTH:
        raise ValueError(
            f"A sigla (especie) deve ter no máximo {ESPECIE_MAX_LENGTH} caracteres."
        )
    return normalized


def normalize_especie_from_db(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    normalized = str(value).strip().upper()
    return normalized or None


class PEspecieSchema(BaseModel):
    especie_id: Optional[int] = None
    especie: Optional[str] = None
    descricao: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class PEspecieIdSchema(BaseModel):
    especie_id: int


class PEspecieIndexSchema(BaseModel):
    """busca: termo único pesquisado em ESPECIE ou DESCRICAO (OR, LIKE)."""

    busca: Optional[str] = None

    model_config = ConfigDict(extra="forbid")

    @field_validator("busca", mode="before")
    @classmethod
    def sanitize_filters(cls, value):
        if value is None or value == "":
            return None
        return Text.sanitize_input(str(value))


class PEspecieEspecieSchema(BaseModel):
    especie: str
    especie_id: Optional[int] = None

    @field_validator("especie")
    @classmethod
    def validate_especie(cls, value: str):
        return normalize_especie(Text.sanitize_input(value))


class PEspecieSaveSchema(BaseModel):
    especie_id: Optional[int] = None
    especie: str
    descricao: str

    @field_validator("especie")
    @classmethod
    def validate_especie(cls, value: str):
        return normalize_especie(Text.sanitize_input(value))

    @field_validator("descricao")
    @classmethod
    def sanitize_descricao(cls, value: str):
        return Text.sanitize_input(value)


class PEspecieUpdateSchema(BaseModel):
    especie: Optional[str] = None
    descricao: Optional[str] = None

    @field_validator("especie")
    @classmethod
    def validate_especie(cls, value: Optional[str]):
        if value is None:
            return value
        return normalize_especie(Text.sanitize_input(value))

    @field_validator("descricao")
    @classmethod
    def sanitize_descricao(cls, value: Optional[str]):
        if value is None:
            return value
        return Text.sanitize_input(value)
