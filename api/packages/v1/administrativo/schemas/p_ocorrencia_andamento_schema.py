from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator, model_validator

from actions.validations.text import Text

CODIGO_MAX_LENGTH = 10


def normalize_codigo(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    normalized = str(value).strip().upper()
    if not normalized:
        raise ValueError("O código é obrigatório.")
    if len(normalized) > CODIGO_MAX_LENGTH:
        raise ValueError(
            f"O código deve ter no máximo {CODIGO_MAX_LENGTH} caracteres."
        )
    return normalized


class POcorrenciaAndamentoSchema(BaseModel):
    ocorrencia_andamento_id: Optional[int] = None
    codigo: Optional[str] = None
    descricao: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class POcorrenciaAndamentoIdSchema(BaseModel):
    ocorrencia_andamento_id: int


class POcorrenciaAndamentoIndexSchema(BaseModel):
    """Filtro: descricao (LIKE em DESCRICAO)."""

    descricao: Optional[str] = None

    model_config = ConfigDict(extra="forbid")

    @field_validator("descricao", mode="before")
    @classmethod
    def sanitize_filters(cls, value):
        if value is None or value == "":
            return None
        return Text.sanitize_input(str(value))


class POcorrenciaAndamentoCodigoSchema(BaseModel):
    codigo: str
    ocorrencia_andamento_id: Optional[int] = None

    @field_validator("codigo")
    @classmethod
    def validate_codigo(cls, value: str):
        return normalize_codigo(Text.sanitize_input(value))


class POcorrenciaAndamentoSaveSchema(BaseModel):
    ocorrencia_andamento_id: Optional[int] = None
    codigo: str
    descricao: str

    @field_validator("codigo", "descricao")
    @classmethod
    def sanitize_fields(cls, value: str):
        return Text.sanitize_input(value)

    @field_validator("codigo", mode="after")
    @classmethod
    def validate_codigo_field(cls, value: str):
        return normalize_codigo(value)

    @model_validator(mode="after")
    def validate_required_fields(self):
        errors = []
        if not self.descricao or not self.descricao.strip():
            errors.append({"input": "descricao", "message": "A descrição é obrigatória."})
        if not self.codigo or not str(self.codigo).strip():
            errors.append({"input": "codigo", "message": "O código é obrigatório."})
        if errors:
            detail = "; ".join(f"{e['input']}: {e['message']}" for e in errors)
            raise ValueError(detail)
        return self


class POcorrenciaAndamentoUpdateSchema(BaseModel):
    codigo: Optional[str] = None
    descricao: Optional[str] = None

    @field_validator("codigo", "descricao")
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
