from datetime import date, datetime
from typing import Optional, Union

from pydantic import BaseModel, ConfigDict, field_validator, model_validator

from actions.validations.text import Text

# G_FERIADO (VARCHAR(1)): tipo F|V; situacao A|I (I/vazio/NULL no banco = inativo)
TIPO_CODIGOS_VALIDOS = frozenset({"F", "V"})
SITUACAO_CODIGOS_VALIDOS = frozenset({"A", "I"})


def normalize_tipo(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    normalized = str(value).strip().upper()
    if not normalized:
        return None
    if normalized not in TIPO_CODIGOS_VALIDOS:
        raise ValueError(
            f"Tipo de feriado inválido: '{value}'. Use F (fixo) ou V (variável)."
        )
    return normalized


def normalize_situacao(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    normalized = str(value).strip().upper()
    if not normalized:
        return None
    if normalized not in SITUACAO_CODIGOS_VALIDOS:
        raise ValueError(
            f"Situação de feriado inválida: '{value}'. Use A (ativo) ou I (inativo)."
        )
    return normalized


class GFeriadoSchema(BaseModel):
    feriado_id: Optional[int] = None
    ano: Optional[int] = None
    mes: Optional[int] = None
    dia: Optional[int] = None
    data: Optional[Union[datetime, date]] = None
    descricao: Optional[str] = None
    tipo: Optional[str] = None
    situacao: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class GFeriadoIdSchema(BaseModel):
    feriado_id: int


class GFeriadoIndexSchema(BaseModel):
    ano: Optional[int] = None
    tipo: Optional[str] = None
    situacao: Optional[str] = None
    descricao: Optional[str] = None

    model_config = ConfigDict(extra="forbid")

    @field_validator("ano", mode="before")
    @classmethod
    def validate_ano(cls, value):
        if value is None or value == "":
            return None
        try:
            return int(value)
        except (TypeError, ValueError) as exc:
            raise ValueError("O filtro ano deve ser um número inteiro.") from exc

    @field_validator("tipo", "situacao", "descricao", mode="before")
    @classmethod
    def sanitize_filters(cls, value):
        if value is None or value == "":
            return None
        return Text.sanitize_input(str(value))

    @field_validator("tipo", mode="after")
    @classmethod
    def validate_tipo_sigla(cls, value: Optional[str]):
        if value is None:
            return value
        try:
            return normalize_tipo(value)
        except ValueError as exc:
            raise ValueError(str(exc)) from exc

    @field_validator("situacao", mode="after")
    @classmethod
    def validate_situacao_sigla(cls, value: Optional[str]):
        if value is None:
            return value
        try:
            return normalize_situacao(value)
        except ValueError as exc:
            raise ValueError(str(exc)) from exc


class GFeriadoDataTipoSchema(BaseModel):
    data: Union[datetime, date]
    tipo: str
    feriado_id: Optional[int] = None

    @field_validator("tipo")
    @classmethod
    def validate_tipo_sigla(cls, value: str):
        sanitized = Text.sanitize_input(value)
        try:
            return normalize_tipo(sanitized)
        except ValueError as exc:
            raise ValueError(str(exc)) from exc


class GFeriadoSaveSchema(BaseModel):
    feriado_id: Optional[int] = None
    data: Union[datetime, date]
    descricao: str
    tipo: str
    situacao: str
    ano: Optional[int] = None
    mes: Optional[int] = None
    dia: Optional[int] = None

    @field_validator("descricao", "tipo", "situacao")
    @classmethod
    def sanitize_fields(cls, value: str):
        return Text.sanitize_input(value)

    @field_validator("tipo", mode="after")
    @classmethod
    def validate_tipo_sigla(cls, value: str):
        try:
            return normalize_tipo(value)
        except ValueError as exc:
            raise ValueError(str(exc)) from exc

    @field_validator("situacao", mode="after")
    @classmethod
    def validate_situacao_sigla(cls, value: str):
        try:
            return normalize_situacao(value)
        except ValueError as exc:
            raise ValueError(str(exc)) from exc

    @model_validator(mode="after")
    def validate_required_fields(self):
        errors = []

        if not self.descricao or not self.descricao.strip():
            errors.append({"input": "descricao", "message": "A descrição é obrigatória."})
        if not self.tipo or not self.tipo.strip():
            errors.append({"input": "tipo", "message": "O tipo é obrigatório."})
        if not self.situacao or not self.situacao.strip():
            errors.append({"input": "situacao", "message": "A situação é obrigatória."})
        if not self.data:
            errors.append({"input": "data", "message": "A data é obrigatória."})

        if errors:
            detail = "; ".join(
                f"{item['input']}: {item['message']}" for item in errors
            )
            raise ValueError(detail)

        parsed = self._parse_data(self.data)
        self.data = parsed
        self.ano = parsed.year
        self.mes = parsed.month
        self.dia = parsed.day
        return self

    @staticmethod
    def _parse_data(value: Union[datetime, date]) -> datetime:
        if isinstance(value, datetime):
            return value.replace(tzinfo=None) if value.tzinfo else value
        return datetime.combine(value, datetime.min.time())


class GFeriadoUpdateSchema(BaseModel):
    data: Optional[Union[datetime, date]] = None
    descricao: Optional[str] = None
    tipo: Optional[str] = None
    situacao: Optional[str] = None
    ano: Optional[int] = None
    mes: Optional[int] = None
    dia: Optional[int] = None

    @field_validator("descricao", "tipo", "situacao")
    @classmethod
    def sanitize_fields(cls, value: Optional[str]):
        if value is None:
            return value
        return Text.sanitize_input(value)

    @field_validator("tipo", mode="after")
    @classmethod
    def validate_tipo_sigla(cls, value: Optional[str]):
        if value is None:
            return value
        try:
            return normalize_tipo(value)
        except ValueError as exc:
            raise ValueError(str(exc)) from exc

    @field_validator("situacao", mode="after")
    @classmethod
    def validate_situacao_sigla(cls, value: Optional[str]):
        if value is None:
            return value
        try:
            return normalize_situacao(value)
        except ValueError as exc:
            raise ValueError(str(exc)) from exc

    @model_validator(mode="after")
    def normalize_data_parts(self):
        if self.data is None:
            return self

        parsed = GFeriadoSaveSchema._parse_data(self.data)
        self.data = parsed
        self.ano = parsed.year
        self.mes = parsed.month
        self.dia = parsed.day
        return self
