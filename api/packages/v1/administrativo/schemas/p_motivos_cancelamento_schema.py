from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator, model_validator

from actions.validations.text import Text
from packages.v1.administrativo.schemas.p_motivos_schema import (
    normalize_situacao,
    situacao_from_db,
    situacao_to_db,
)

__all__ = [
    "normalize_situacao",
    "situacao_from_db",
    "situacao_to_db",
    "PMotivosCancelamentoSchema",
    "PMotivosCancelamentoIdSchema",
    "PMotivosCancelamentoIndexSchema",
    "PMotivosCancelamentoSaveSchema",
    "PMotivosCancelamentoUpdateSchema",
]


class PMotivosCancelamentoSchema(BaseModel):
    motivos_cancelamento_id: Optional[int] = None
    descricao: Optional[str] = None
    situacao: Optional[str] = None
    total_titulos: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class PMotivosCancelamentoIdSchema(BaseModel):
    motivos_cancelamento_id: int


class PMotivosCancelamentoIndexSchema(BaseModel):
    """Filtro de negócio: apenas descricao (LIKE em DESCRICAO)."""

    descricao: Optional[str] = None

    model_config = ConfigDict(extra="forbid")

    @field_validator("descricao", mode="before")
    @classmethod
    def sanitize_descricao(cls, value):
        if value is None or value == "":
            return None
        return Text.sanitize_input(str(value))


class PMotivosCancelamentoSaveSchema(BaseModel):
    motivos_cancelamento_id: Optional[int] = None
    descricao: str
    situacao: str

    @field_validator("descricao", "situacao")
    @classmethod
    def sanitize_fields(cls, value: str):
        return Text.sanitize_input(value)

    @field_validator("situacao", mode="after")
    @classmethod
    def validate_situacao_sigla(cls, value: str):
        return normalize_situacao(value)

    @model_validator(mode="after")
    def validate_required_fields(self):
        errors = []
        if not self.descricao or not self.descricao.strip():
            errors.append(
                {"input": "descricao", "message": "A descrição é obrigatória."}
            )
        if not self.situacao or not self.situacao.strip():
            errors.append(
                {"input": "situacao", "message": "A situação é obrigatória."}
            )
        if errors:
            detail = "; ".join(f"{e['input']}: {e['message']}" for e in errors)
            raise ValueError(detail)
        return self


class PMotivosCancelamentoUpdateSchema(BaseModel):
    descricao: Optional[str] = None
    situacao: Optional[str] = None

    @field_validator("descricao", "situacao")
    @classmethod
    def sanitize_fields(cls, value: Optional[str]):
        if value is None:
            return value
        return Text.sanitize_input(value)

    @field_validator("situacao", mode="after")
    @classmethod
    def validate_situacao_sigla(cls, value: Optional[str]):
        if value is None:
            return value
        return normalize_situacao(value)
