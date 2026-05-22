from __future__ import annotations

from datetime import date, datetime
from typing import Optional, Union

from pydantic import BaseModel, ConfigDict, field_validator, model_validator

from actions.validations.text import Text

# P_ANDAMENTO.ARQUIVO_GERADO VARCHAR(1) — D = Aguardando; E = Exportado
ARQUIVO_GERADO_AGUARDANDO = "D"
ARQUIVO_GERADO_EXPORTADO = "E"
ARQUIVO_GERADO_CODIGOS_VALIDOS = frozenset(
    {ARQUIVO_GERADO_AGUARDANDO, ARQUIVO_GERADO_EXPORTADO}
)


def normalize_arquivo_gerado(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    normalized = str(value).strip().upper()
    if not normalized:
        return None
    if normalized not in ARQUIVO_GERADO_CODIGOS_VALIDOS:
        raise ValueError(
            f"Arquivo gerado inválido: '{value}'. Use D (aguardando) ou E (exportado)."
        )
    return normalized


def arquivo_gerado_from_db(value: Optional[str]) -> Optional[str]:
    if value is None or not str(value).strip():
        return None
    return normalize_arquivo_gerado(str(value).strip())


def _to_naive_datetime(value: Union[datetime, date]) -> datetime:
    if isinstance(value, datetime):
        return value.replace(tzinfo=None) if value.tzinfo else value
    return datetime.combine(value, datetime.min.time())


def _is_date_only(value: datetime) -> bool:
    return (
        value.hour == 0
        and value.minute == 0
        and value.second == 0
        and value.microsecond == 0
    )


class PAndamentoSchema(BaseModel):
    andamento_id: Optional[int] = None
    ocorrencia_andamento_id: Optional[int] = None
    data_ocorrencia: Optional[datetime] = None
    titulo_id: Optional[int] = None
    usuario_id: Optional[int] = None
    arquivo_gerado: Optional[str] = None
    data_geracao: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class PAndamentoIdSchema(BaseModel):
    andamento_id: int


class PAndamentoTituloIdSchema(BaseModel):
    titulo_id: int


class PAndamentoIndexByTituloSchema(BaseModel):
    """Filtros opcionais na listagem por título (titulo_id vem no path)."""

    data_ocorrencia: Optional[Union[datetime, date]] = None
    ocorrencia_andamento_id: Optional[int] = None

    model_config = ConfigDict(extra="forbid")

    @field_validator("ocorrencia_andamento_id", mode="before")
    @classmethod
    def parse_ocorrencia_andamento_id(cls, value):
        if value is None or value == "":
            return None
        return int(value)

    @field_validator("data_ocorrencia", mode="after")
    @classmethod
    def parse_data_ocorrencia_filter(
        cls, value: Optional[Union[datetime, date]]
    ) -> Optional[datetime]:
        if value is None:
            return None
        return _to_naive_datetime(value)


class PAndamentoIndexSchema(BaseModel):
    """Filtros: titulo_id, data_ocorrencia (dia ou timestamp), ocorrencia_andamento_id."""

    titulo_id: Optional[int] = None
    data_ocorrencia: Optional[Union[datetime, date]] = None
    ocorrencia_andamento_id: Optional[int] = None

    model_config = ConfigDict(extra="forbid")

    @field_validator("titulo_id", "ocorrencia_andamento_id", mode="before")
    @classmethod
    def parse_optional_int(cls, value):
        if value is None or value == "":
            return None
        return int(value)

    @field_validator("data_ocorrencia", mode="after")
    @classmethod
    def parse_data_ocorrencia_filter(
        cls, value: Optional[Union[datetime, date]]
    ) -> Optional[datetime]:
        if value is None:
            return None
        return _to_naive_datetime(value)


class PAndamentoSaveSchema(BaseModel):
    andamento_id: Optional[int] = None
    ocorrencia_andamento_id: int
    data_ocorrencia: Union[datetime, date]
    titulo_id: int
    usuario_id: int
    arquivo_gerado: str = ARQUIVO_GERADO_AGUARDANDO
    data_geracao: Optional[Union[datetime, date]] = None

    @field_validator("arquivo_gerado", mode="before")
    @classmethod
    def sanitize_arquivo_gerado(cls, value):
        if value is None:
            return ARQUIVO_GERADO_AGUARDANDO
        return Text.sanitize_input(str(value))

    @field_validator("arquivo_gerado", mode="after")
    @classmethod
    def validate_arquivo_gerado(cls, value: str):
        return normalize_arquivo_gerado(value) or ARQUIVO_GERADO_AGUARDANDO

    @field_validator("data_ocorrencia", "data_geracao", mode="after")
    @classmethod
    def parse_datetimes(
        cls, value: Optional[Union[datetime, date]]
    ) -> Optional[datetime]:
        if value is None:
            return None
        return _to_naive_datetime(value)

    @model_validator(mode="after")
    def validate_required_fields(self):
        errors = []
        if self.titulo_id is None:
            errors.append({"input": "titulo_id", "message": "O título é obrigatório."})
        if self.ocorrencia_andamento_id is None:
            errors.append(
                {
                    "input": "ocorrencia_andamento_id",
                    "message": "A ocorrência de andamento é obrigatória.",
                }
            )
        if self.usuario_id is None:
            errors.append({"input": "usuario_id", "message": "O usuário é obrigatório."})
        if self.data_ocorrencia is None:
            errors.append(
                {"input": "data_ocorrencia", "message": "A data de ocorrência é obrigatória."}
            )
        if errors:
            detail = "; ".join(f"{e['input']}: {e['message']}" for e in errors)
            raise ValueError(detail)
        return self


class PAndamentoUpdateSchema(BaseModel):
    ocorrencia_andamento_id: Optional[int] = None
    data_ocorrencia: Optional[Union[datetime, date]] = None
    titulo_id: Optional[int] = None
    usuario_id: Optional[int] = None
    arquivo_gerado: Optional[str] = None
    data_geracao: Optional[Union[datetime, date]] = None

    @field_validator("arquivo_gerado", mode="before")
    @classmethod
    def sanitize_arquivo_gerado(cls, value: Optional[str]):
        if value is None:
            return value
        return Text.sanitize_input(str(value))

    @field_validator("arquivo_gerado", mode="after")
    @classmethod
    def validate_arquivo_gerado(cls, value: Optional[str]):
        if value is None:
            return None
        return normalize_arquivo_gerado(value)

    @field_validator("data_ocorrencia", "data_geracao", mode="after")
    @classmethod
    def parse_datetimes(
        cls, value: Optional[Union[datetime, date]]
    ) -> Optional[datetime]:
        if value is None:
            return None
        return _to_naive_datetime(value)
