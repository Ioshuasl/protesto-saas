from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator, model_validator

from actions.validations.text import Text

# P_MOTIVOS: SITUACAO VARCHAR(15) — API A (ativo); I ou NULL no banco = inativo na resposta
SITUACAO_CODIGO_ATIVO = "A"
SITUACAO_CODIGO_INATIVO = "I"
SITUACAO_CODIGOS_VALIDOS = frozenset({SITUACAO_CODIGO_ATIVO, SITUACAO_CODIGO_INATIVO})
CODIGO_MAX_LENGTH = 3


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


def situacao_to_db(value: str) -> Optional[str]:
    """Persistência: A no banco; inativo grava NULL."""
    code = normalize_situacao(value)
    if code is None:
        return None
    if code == SITUACAO_CODIGO_ATIVO:
        return SITUACAO_CODIGO_ATIVO
    return None


def situacao_from_db(value: Optional[str]) -> str:
    if value is None or not str(value).strip():
        return SITUACAO_CODIGO_INATIVO
    normalized = str(value).strip().upper()
    if normalized == SITUACAO_CODIGO_ATIVO:
        return SITUACAO_CODIGO_ATIVO
    return SITUACAO_CODIGO_INATIVO


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


class PMotivosSchema(BaseModel):
    motivos_id: Optional[int] = None
    descricao: Optional[str] = None
    situacao: Optional[str] = None
    codigo: Optional[str] = None
    total_titulos: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class PMotivosIdSchema(BaseModel):
    motivos_id: int


class PMotivosIndexSchema(BaseModel):
    """Filtros: descricao (LIKE em DESCRICAO); situacao A (ativo) ou I (inativo)."""

    descricao: Optional[str] = None
    situacao: Optional[str] = None

    model_config = ConfigDict(extra="forbid")

    @field_validator("descricao", "situacao", mode="before")
    @classmethod
    def sanitize_filters(cls, value):
        if value is None or value == "":
            return None
        return Text.sanitize_input(str(value))

    @field_validator("situacao", mode="after")
    @classmethod
    def validate_situacao_filter(cls, value: Optional[str]):
        if value is None:
            return None
        return normalize_situacao(value)


class PMotivosCodigoSchema(BaseModel):
    codigo: str
    motivos_id: Optional[int] = None

    @field_validator("codigo")
    @classmethod
    def validate_codigo(cls, value: str):
        return normalize_codigo(Text.sanitize_input(value))


class PMotivosSaveSchema(BaseModel):
    motivos_id: Optional[int] = None
    codigo: str
    descricao: str
    situacao: str

    @field_validator("codigo", "descricao", "situacao")
    @classmethod
    def sanitize_fields(cls, value: str):
        return Text.sanitize_input(value)

    @field_validator("codigo", mode="after")
    @classmethod
    def validate_codigo_field(cls, value: str):
        return normalize_codigo(value)

    @field_validator("situacao", mode="after")
    @classmethod
    def validate_situacao_sigla(cls, value: str):
        return normalize_situacao(value)

    @model_validator(mode="after")
    def validate_required_fields(self):
        errors = []
        if not self.descricao or not self.descricao.strip():
            errors.append({"input": "descricao", "message": "A descrição é obrigatória."})
        if not self.codigo or not str(self.codigo).strip():
            errors.append({"input": "codigo", "message": "O código é obrigatório."})
        if not self.situacao or not self.situacao.strip():
            errors.append({"input": "situacao", "message": "A situação é obrigatória."})
        if errors:
            detail = "; ".join(f"{e['input']}: {e['message']}" for e in errors)
            raise ValueError(detail)
        return self


class PMotivosUpdateSchema(BaseModel):
    codigo: Optional[str] = None
    descricao: Optional[str] = None
    situacao: Optional[str] = None

    @field_validator("codigo", "descricao", "situacao")
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

    @field_validator("situacao", mode="after")
    @classmethod
    def validate_situacao_sigla(cls, value: Optional[str]):
        if value is None:
            return value
        return normalize_situacao(value)
