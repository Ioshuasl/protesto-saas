from datetime import date, datetime
from typing import Optional, Union

from pydantic import BaseModel, ConfigDict, field_validator

from actions.validations.text import Text

SIGLA_MAX_LENGTH = 3
ABERTO_CODIGOS_VALIDOS = frozenset({"S", "N"})


def normalize_sigla(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    normalized = str(value).strip().upper()
    if not normalized:
        return None
    if len(normalized) > SIGLA_MAX_LENGTH:
        raise ValueError(
            f"A sigla deve ter no máximo {SIGLA_MAX_LENGTH} caracteres."
        )
    return normalized


def normalize_aberto(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    normalized = str(value).strip().upper()
    if not normalized:
        return None
    if normalized not in ABERTO_CODIGOS_VALIDOS:
        raise ValueError(
            f"Filtro aberto inválido: '{value}'. Use S (aberto) ou N (fechado)."
        )
    return normalized


def is_livro_aberto(data_fechamento) -> bool:
    if data_fechamento is None:
        return True
    if isinstance(data_fechamento, str) and not str(data_fechamento).strip():
        return True
    return False


class PLivroAndamentoSchema(BaseModel):
    livro_andamento_id: Optional[int] = None
    livro_natureza_id: Optional[int] = None
    folha_atual: Optional[int] = None
    numero_livro: Optional[int] = None
    data_abertura: Optional[Union[datetime, date]] = None
    data_fechamento: Optional[Union[datetime, date]] = None
    numero_folhas: Optional[int] = None
    sigla: Optional[str] = None
    usuario_id: Optional[int] = None
    aberto: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)


class PLivroAndamentoIdSchema(BaseModel):
    livro_andamento_id: int


class PLivroAndamentoNaturezaIdSchema(BaseModel):
    livro_natureza_id: int


class PLivroAndamentoIndexSchema(BaseModel):
    busca: Optional[str] = None
    livro_natureza_id: Optional[int] = None
    aberto: Optional[str] = None

    model_config = ConfigDict(extra="forbid")

    @field_validator("busca", mode="before")
    @classmethod
    def sanitize_busca(cls, value):
        if value is None or value == "":
            return None
        return Text.sanitize_input(str(value))

    @field_validator("livro_natureza_id", mode="before")
    @classmethod
    def validate_livro_natureza_id(cls, value):
        if value is None or value == "":
            return None
        return int(value)

    @field_validator("aberto", mode="after")
    @classmethod
    def validate_aberto(cls, value: Optional[str]):
        if value is None:
            return value
        try:
            return normalize_aberto(value)
        except ValueError as exc:
            raise ValueError(str(exc)) from exc


class PLivroAndamentoSaveSchema(BaseModel):
    livro_andamento_id: Optional[int] = None
    livro_natureza_id: int
    folha_atual: int
    numero_livro: int
    numero_folhas: int
    data_abertura: Union[datetime, date]
    data_fechamento: Optional[Union[datetime, date]] = None
    sigla: Optional[str] = None
    usuario_id: Optional[int] = None

    @field_validator("sigla")
    @classmethod
    def validate_sigla(cls, value: Optional[str]):
        if value is None:
            return value
        return normalize_sigla(Text.sanitize_input(value))

    @field_validator("data_abertura", mode="after")
    @classmethod
    def parse_data_abertura(cls, value: Union[datetime, date]) -> datetime:
        if isinstance(value, datetime):
            return value.replace(tzinfo=None) if value.tzinfo else value
        return datetime.combine(value, datetime.min.time())

    @field_validator("data_fechamento", mode="after")
    @classmethod
    def parse_data_fechamento(
        cls, value: Optional[Union[datetime, date]]
    ) -> Optional[datetime]:
        if value is None:
            return None
        if isinstance(value, datetime):
            return value.replace(tzinfo=None) if value.tzinfo else value
        return datetime.combine(value, datetime.min.time())


class PLivroAndamentoUpdateSchema(BaseModel):
    livro_natureza_id: Optional[int] = None
    folha_atual: Optional[int] = None
    numero_livro: Optional[int] = None
    numero_folhas: Optional[int] = None
    data_abertura: Optional[Union[datetime, date]] = None
    data_fechamento: Optional[Union[datetime, date]] = None
    sigla: Optional[str] = None
    usuario_id: Optional[int] = None

    @field_validator("sigla")
    @classmethod
    def validate_sigla(cls, value: Optional[str]):
        if value is None:
            return value
        return normalize_sigla(Text.sanitize_input(value))

    @field_validator("data_abertura", mode="after")
    @classmethod
    def parse_data_abertura(
        cls, value: Optional[Union[datetime, date]]
    ) -> Optional[datetime]:
        if value is None:
            return None
        if isinstance(value, datetime):
            return value.replace(tzinfo=None) if value.tzinfo else value
        return datetime.combine(value, datetime.min.time())

    @field_validator("data_fechamento", mode="after")
    @classmethod
    def parse_data_fechamento(
        cls, value: Optional[Union[datetime, date]]
    ) -> Optional[datetime]:
        if value is None:
            return None
        if isinstance(value, datetime):
            return value.replace(tzinfo=None) if value.tzinfo else value
        return datetime.combine(value, datetime.min.time())
