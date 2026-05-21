from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator

from actions.validations.text import Text

SIGLA_MAX_LENGTH = 3
SITUACAO_CODIGO_ATIVO = "A"
SITUACAO_CODIGO_INATIVO = "I"
SITUACAO_CODIGOS_VALIDOS = frozenset({SITUACAO_CODIGO_ATIVO, SITUACAO_CODIGO_INATIVO})


def normalize_sigla(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    normalized = str(value).strip().upper()
    if not normalized:
        raise ValueError("A sigla é obrigatória.")
    if len(normalized) > SIGLA_MAX_LENGTH:
        raise ValueError(
            f"A sigla deve ter no máximo {SIGLA_MAX_LENGTH} caracteres."
        )
    return normalized


def normalize_sigla_from_db(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    normalized = str(value).strip().upper()
    return normalized or None


def normalize_situacao(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    normalized = str(value).strip().upper()
    if not normalized:
        return None
    if normalized not in SITUACAO_CODIGOS_VALIDOS:
        raise ValueError(
            f"Situação inválida: '{value}'. Use A (ativo) ou I (inativo)."
        )
    return normalized


def situacao_from_db(value: Optional[str]) -> str:
    if value is None or not str(value).strip():
        return SITUACAO_CODIGO_INATIVO
    code = str(value).strip().upper()
    if code == SITUACAO_CODIGO_ATIVO:
        return SITUACAO_CODIGO_ATIVO
    return SITUACAO_CODIGO_INATIVO


def situacao_to_db(value: str) -> Optional[str]:
    code = normalize_situacao(value)
    if code == SITUACAO_CODIGO_ATIVO:
        return SITUACAO_CODIGO_ATIVO
    return None


class PLivroNaturezaSchema(BaseModel):
    livro_natureza_id: Optional[int] = None
    sigla: Optional[str] = None
    descricao: Optional[str] = None
    situacao: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class PLivroNaturezaIdSchema(BaseModel):
    livro_natureza_id: int


class PLivroNaturezaIndexSchema(BaseModel):
    """busca: termo único pesquisado em SIGLA ou DESCRICAO (OR, LIKE)."""

    busca: Optional[str] = None

    model_config = ConfigDict(extra="forbid")

    @field_validator("busca", mode="before")
    @classmethod
    def sanitize_filters(cls, value):
        if value is None or value == "":
            return None
        return Text.sanitize_input(str(value))


class PLivroNaturezaSaveSchema(BaseModel):
    livro_natureza_id: Optional[int] = None
    sigla: str
    descricao: str
    situacao: str

    @field_validator("sigla")
    @classmethod
    def validate_sigla(cls, value: str):
        return normalize_sigla(Text.sanitize_input(value))

    @field_validator("descricao")
    @classmethod
    def sanitize_descricao(cls, value: str):
        sanitized = Text.sanitize_input(value)
        if not sanitized or not sanitized.strip():
            raise ValueError("A descrição é obrigatória.")
        return sanitized

    @field_validator("situacao")
    @classmethod
    def validate_situacao(cls, value: str):
        return normalize_situacao(Text.sanitize_input(value))


class PLivroNaturezaUpdateSchema(BaseModel):
    sigla: Optional[str] = None
    descricao: Optional[str] = None
    situacao: Optional[str] = None

    @field_validator("sigla")
    @classmethod
    def validate_sigla(cls, value: Optional[str]):
        if value is None:
            return value
        return normalize_sigla(Text.sanitize_input(value))

    @field_validator("descricao")
    @classmethod
    def sanitize_descricao(cls, value: Optional[str]):
        if value is None:
            return value
        sanitized = Text.sanitize_input(value)
        if not sanitized or not sanitized.strip():
            raise ValueError("A descrição não pode ser vazia.")
        return sanitized

    @field_validator("situacao")
    @classmethod
    def validate_situacao(cls, value: Optional[str]):
        if value is None:
            return value
        return normalize_situacao(Text.sanitize_input(value))
