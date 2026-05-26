from __future__ import annotations

from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator

from actions.validations.text import Text

TIPOS_CERTIDAO = {"R", "P", "N"}
TIPOS_CERTIDAO_INDEX = {"P", "N"}
TIPOS_REMESSA = {"P", "C"}
STATUS_CERTIDAO = {"A", "C"}


def _sanitize_optional_text(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    sanitized = Text.sanitize_input(str(value)).strip()
    return sanitized or None


def _normalize_sigla(value: Optional[str]) -> Optional[str]:
    sanitized = _sanitize_optional_text(value)
    if sanitized is None:
        return None
    return sanitized.upper()


def normalize_tipo_certidao(value: Optional[str]) -> Optional[str]:
    sigla = _normalize_sigla(value)
    if sigla is None:
        return None
    if sigla not in TIPOS_CERTIDAO:
        raise ValueError("tipo_certidao deve ser R, P ou N.")
    return sigla


def normalize_tipo_certidao_index(value: Optional[str]) -> Optional[str]:
    sigla = _normalize_sigla(value)
    if sigla is None:
        return None
    if sigla not in TIPOS_CERTIDAO_INDEX:
        raise ValueError("tipo_certidao deve ser P ou N.")
    return sigla


def normalize_tipo_remessa(value: Optional[str]) -> Optional[str]:
    sigla = _normalize_sigla(value)
    if sigla is None:
        return None
    if sigla not in TIPOS_REMESSA:
        raise ValueError("tipo_remessa deve ser P ou C.")
    return sigla


def normalize_status(value: Optional[str]) -> Optional[str]:
    sigla = _normalize_sigla(value)
    if sigla is None:
        return None
    if sigla not in STATUS_CERTIDAO:
        raise ValueError("status deve ser A ou C.")
    return sigla


class PCertidaoSchema(BaseModel):
    certidao_id: Optional[int] = None
    usuario_id: Optional[int] = None
    data_certidao: Optional[date] = None
    hora_certidao: Optional[str] = None
    tipo_certidao: Optional[str] = None
    valor_emolumento: Optional[float] = None
    valor_taxa_judiciaria: Optional[float] = None
    valor_fundesp: Optional[float] = None
    valor_taxa_extra: Optional[float] = None
    numero_impressao: Optional[int] = None
    cpfcnpj: Optional[str] = None
    nome: Optional[str] = None
    status: Optional[str] = None
    observacao: Optional[str] = None
    valor_taxa_iss: Optional[float] = None
    apresentante: Optional[str] = None
    nfse_id: Optional[int] = None
    qtd_protestos: Optional[int] = None
    qtd_cancelados: Optional[int] = None
    qtd_sustado: Optional[int] = None
    n_remessa: Optional[int] = None
    tipo_remessa: Optional[str] = None
    protecao_credito_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class PCertidaoIdSchema(BaseModel):
    certidao_id: int


class PCertidaoIndexSchema(BaseModel):
    """Filtros de negócio do index; formato3 fica no QueryParamsParser."""

    tipo_certidao: Optional[str] = None
    data_certidao: Optional[date] = None
    data_inicio: Optional[date] = None
    data_fim: Optional[date] = None
    status: Optional[str] = None
    busca: Optional[str] = None

    model_config = ConfigDict(extra="forbid")

    @field_validator("tipo_certidao", mode="after")
    @classmethod
    def validate_tipo_certidao(cls, value: Optional[str]) -> Optional[str]:
        return normalize_tipo_certidao_index(value)

    @field_validator("status", mode="after")
    @classmethod
    def validate_status(cls, value: Optional[str]) -> Optional[str]:
        return normalize_status(value)

    @field_validator("busca", mode="before")
    @classmethod
    def sanitize_busca(cls, value: Optional[str]) -> Optional[str]:
        return _sanitize_optional_text(value)


class PCertidaoConsultaApresentanteSchema(BaseModel):
    apresentante: str
    cpfcnpj: str
    data_inicio: Optional[date] = None
    data_fim: Optional[date] = None

    @field_validator("apresentante", "cpfcnpj", mode="before")
    @classmethod
    def sanitize_required_text(cls, value: str) -> str:
        sanitized = Text.sanitize_input(str(value)).strip()
        if not sanitized:
            raise ValueError("Campo obrigatório.")
        return sanitized


class PCertidaoSaveSchema(PCertidaoSchema):
    @field_validator(
        "hora_certidao",
        "cpfcnpj",
        "nome",
        "observacao",
        "apresentante",
        mode="before",
    )
    @classmethod
    def sanitize_text_fields(cls, value: Optional[str]) -> Optional[str]:
        return _sanitize_optional_text(value)

    @field_validator("tipo_certidao", mode="after")
    @classmethod
    def validate_tipo_certidao(cls, value: Optional[str]) -> Optional[str]:
        return normalize_tipo_certidao(value)

    @field_validator("tipo_remessa", mode="after")
    @classmethod
    def validate_tipo_remessa(cls, value: Optional[str]) -> Optional[str]:
        return normalize_tipo_remessa(value)

    @field_validator("status", mode="after")
    @classmethod
    def validate_status(cls, value: Optional[str]) -> Optional[str]:
        return normalize_status(value)


class PCertidaoUpdateSchema(PCertidaoSaveSchema):
    certidao_id: None = None
