from __future__ import annotations

import unicodedata
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator, model_validator

from actions.validations.text import Text

# TIPO VARCHAR(30) — vazio permitido; valores novos na API (uppercase, sem acento)
TIPO_CODIGOS_VALIDOS = frozenset(
    {
        "CADASTRO",
        "APONTADO",
        "INTIMACAO",
        "ACEITE",
        "DESISTENCIA",
        "PAGAMENTO",
        "CANCELAMENTO",
    }
)
CODIGO_MAX_LENGTH = 10
DESCRICAO_MAX_LENGTH = 260


def _strip_accents(value: str) -> str:
    normalized = unicodedata.normalize("NFD", value)
    return "".join(
        char for char in normalized if unicodedata.category(char) != "Mn"
    )


def normalize_tipo(value: Optional[str], *, allow_empty: bool = True) -> Optional[str]:
    if value is None:
        return None
    stripped = str(value).strip()
    if not stripped:
        if allow_empty:
            return None
        raise ValueError("O tipo é obrigatório.")
    canonical = _strip_accents(stripped).upper()
    if canonical not in TIPO_CODIGOS_VALIDOS:
        allowed = ", ".join(sorted(TIPO_CODIGOS_VALIDOS))
        raise ValueError(
            f"Tipo inválido: '{value}'. Valores permitidos: {allowed}."
        )
    return canonical


def tipo_from_db(value: Optional[str]) -> Optional[str]:
    if value is None or not str(value).strip():
        return None
    return str(value).strip()


def tipo_to_db(value: Optional[str]) -> Optional[str]:
    return normalize_tipo(value, allow_empty=True)


def normalize_codigo(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    normalized = str(value).strip()
    if not normalized:
        raise ValueError("O código é obrigatório.")
    if len(normalized) > CODIGO_MAX_LENGTH:
        raise ValueError(
            f"O código deve ter no máximo {CODIGO_MAX_LENGTH} caracteres."
        )
    return normalized


class POcorrenciasSchema(BaseModel):
    ocorrencias_id: Optional[int] = None
    codigo: Optional[str] = None
    descricao: Optional[str] = None
    tipo: Optional[str] = None
    total_titulos: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class POcorrenciasIdSchema(BaseModel):
    ocorrencias_id: int


class POcorrenciasIndexSchema(BaseModel):
    """Filtros: busca (LIKE em DESCRICAO ou CODIGO); tipo (igualdade exata)."""

    busca: Optional[str] = None
    tipo: Optional[str] = None

    model_config = ConfigDict(extra="forbid")

    @field_validator("busca", "tipo", mode="before")
    @classmethod
    def sanitize_filters(cls, value):
        if value is None or value == "":
            return None
        return Text.sanitize_input(str(value))

    @field_validator("tipo", mode="after")
    @classmethod
    def validate_tipo_filter(cls, value: Optional[str]):
        if value is None:
            return None
        return normalize_tipo(value, allow_empty=False)


class POcorrenciasCodigoSchema(BaseModel):
    codigo: str
    ocorrencias_id: Optional[int] = None

    @field_validator("codigo")
    @classmethod
    def validate_codigo(cls, value: str):
        return normalize_codigo(Text.sanitize_input(value))


class POcorrenciasSaveSchema(BaseModel):
    ocorrencias_id: Optional[int] = None
    codigo: str
    descricao: str
    tipo: Optional[str] = None

    @field_validator("codigo", "descricao", "tipo")
    @classmethod
    def sanitize_fields(cls, value: Optional[str]):
        if value is None:
            return value
        return Text.sanitize_input(value)

    @field_validator("codigo", mode="after")
    @classmethod
    def validate_codigo_field(cls, value: str):
        return normalize_codigo(value)

    @field_validator("tipo", mode="after")
    @classmethod
    def validate_tipo_field(cls, value: Optional[str]):
        if value is None:
            return None
        return normalize_tipo(value, allow_empty=True)

    @model_validator(mode="after")
    def validate_required_fields(self):
        errors = []
        if not self.descricao or not self.descricao.strip():
            errors.append(
                {"input": "descricao", "message": "A descrição é obrigatória."}
            )
        if not self.codigo or not str(self.codigo).strip():
            errors.append({"input": "codigo", "message": "O código é obrigatório."})
        if errors:
            detail = "; ".join(f"{e['input']}: {e['message']}" for e in errors)
            raise ValueError(detail)
        return self


class POcorrenciasUpdateSchema(BaseModel):
    codigo: Optional[str] = None
    descricao: Optional[str] = None
    tipo: Optional[str] = None

    @field_validator("codigo", "descricao", "tipo")
    @classmethod
    def sanitize_fields(cls, value: Optional[str]):
        if value is None:
            return value
        return Text.sanitize_input(value)

    @field_validator("codigo", mode="after")
    @classmethod
    def validate_codigo_field(cls, value: Optional[str]):
        if value is None:
            return value
        return normalize_codigo(value)

    @field_validator("tipo", mode="after")
    @classmethod
    def validate_tipo_field(cls, value: Optional[str]):
        if value is None:
            return value
        return normalize_tipo(value, allow_empty=True)
