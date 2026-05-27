from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, ConfigDict, field_validator, model_validator

from actions.validations.text import Text

SITUACAO_CODIGOS_VALIDOS = frozenset({"A", "I"})


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


class GSistemaSchema(BaseModel):
    sistema_id: Optional[Union[int, float]] = None
    descricao: Optional[str] = None
    situacao: Optional[str] = None
    tipo_cartorio: Optional[str] = None
    versao: Optional[str] = None
    data_versao: Optional[datetime] = None
    nome_exe: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class GSistemaIdSchema(BaseModel):
    sistema_id: Union[int, float]


class GSistemaIndexSchema(BaseModel):
    descricao: Optional[str] = None
    situacao: Optional[str] = None
    tipo_cartorio: Optional[str] = None

    model_config = ConfigDict(extra="forbid")

    @field_validator("descricao", "situacao", "tipo_cartorio", mode="before")
    @classmethod
    def sanitize_filters(cls, value):
        if value is None or value == "":
            return None
        return Text.sanitize_input(str(value))

    @field_validator("situacao", mode="after")
    @classmethod
    def validate_situacao_sigla(cls, value: Optional[str]):
        if value is None:
            return value
        try:
            return normalize_situacao(value)
        except ValueError as exc:
            raise ValueError(str(exc)) from exc


class GSistemaSaveSchema(BaseModel):
    sistema_id: Union[int, float]
    descricao: str
    situacao: str
    tipo_cartorio: str
    versao: Optional[str] = None
    data_versao: Optional[datetime] = None
    nome_exe: Optional[str] = None

    @field_validator("descricao", "situacao", "tipo_cartorio", "versao", "nome_exe")
    @classmethod
    def sanitize_fields(cls, value: Optional[str]):
        if value is None:
            return value
        return Text.sanitize_input(value)

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
        if not self.situacao or not self.situacao.strip():
            errors.append({"input": "situacao", "message": "A situação é obrigatória."})
        if not self.tipo_cartorio or not self.tipo_cartorio.strip():
            errors.append(
                {"input": "tipo_cartorio", "message": "O tipo de cartório é obrigatório."}
            )
        if self.sistema_id is None:
            errors.append({"input": "sistema_id", "message": "O ID do sistema é obrigatório."})

        if errors:
            detail = "; ".join(
                f"{item['input']}: {item['message']}" for item in errors
            )
            raise ValueError(detail)

        return self


class GSistemaUpdateSchema(BaseModel):
    descricao: Optional[str] = None
    situacao: Optional[str] = None
    tipo_cartorio: Optional[str] = None
    versao: Optional[str] = None
    data_versao: Optional[datetime] = None
    nome_exe: Optional[str] = None

    @field_validator("descricao", "situacao", "tipo_cartorio", "versao", "nome_exe")
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
        try:
            return normalize_situacao(value)
        except ValueError as exc:
            raise ValueError(str(exc)) from exc
