from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator

from actions.validations.text import Text

# P_BANCO: APONTAMENTO_PAG_POSTERIOR e CUSTAS_NA_CONFIRMACAO — VARCHAR(1): S = sim, N/null = não
SIM_CODIGO = "S"
NAO_CODIGO = "N"
SIM_NAO_CODIGOS = frozenset({SIM_CODIGO, NAO_CODIGO})


def normalize_sim_nao(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    normalized = str(value).strip().upper()
    if not normalized:
        return NAO_CODIGO
    if normalized not in SIM_NAO_CODIGOS:
        raise ValueError(
            f"Valor inválido: '{value}'. Use S (sim) ou N (não)."
        )
    return normalized


def normalize_sim_nao_from_db(value: Optional[str]) -> str:
    if value is None or not str(value).strip():
        return NAO_CODIGO
    normalized = str(value).strip().upper()
    if normalized == SIM_CODIGO:
        return SIM_CODIGO
    return NAO_CODIGO


class PBancoSchema(BaseModel):
    banco_id: Optional[int] = None
    codigo_banco: Optional[str] = None
    descricao: Optional[str] = None
    layout_id: Optional[int] = None
    apontamento_pag_posterior: Optional[str] = None
    custas_na_confirmacao: Optional[str] = None
    pessoa_id: Optional[int] = None
    demais_despesas: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)


class PBancoIdSchema(BaseModel):
    banco_id: int


class PBancoIndexSchema(BaseModel):
    """busca: termo único pesquisado em CODIGO_BANCO ou DESCRICAO (OR, LIKE)."""

    busca: Optional[str] = None

    model_config = ConfigDict(extra="forbid")

    @field_validator("busca", mode="before")
    @classmethod
    def sanitize_filters(cls, value):
        if value is None or value == "":
            return None
        return Text.sanitize_input(str(value))


class PBancoCodigoSchema(BaseModel):
    codigo_banco: str
    banco_id: Optional[int] = None

    @field_validator("codigo_banco")
    @classmethod
    def sanitize_codigo(cls, value: str):
        return Text.sanitize_input(value)


class PBancoLayoutIdSchema(BaseModel):
    layout_id: int


class PBancoSaveSchema(BaseModel):
    banco_id: Optional[int] = None
    codigo_banco: str
    descricao: str
    layout_id: int
    apontamento_pag_posterior: str
    custas_na_confirmacao: str

    @field_validator("codigo_banco", "descricao")
    @classmethod
    def sanitize_fields(cls, value: str):
        return Text.sanitize_input(value)

    @field_validator("apontamento_pag_posterior", "custas_na_confirmacao")
    @classmethod
    def validate_sim_nao_fields(cls, value: str):
        return normalize_sim_nao(value)

    @field_validator("layout_id", mode="before")
    @classmethod
    def validate_layout_id(cls, value):
        try:
            layout_id = int(value)
        except (TypeError, ValueError) as exc:
            raise ValueError("O layout_id deve ser um número inteiro.") from exc
        if layout_id <= 0:
            raise ValueError("O layout_id deve ser maior que zero.")
        return layout_id


class PBancoUpdateSchema(BaseModel):
    codigo_banco: Optional[str] = None
    descricao: Optional[str] = None
    layout_id: Optional[int] = None
    apontamento_pag_posterior: Optional[str] = None
    custas_na_confirmacao: Optional[str] = None

    @field_validator("codigo_banco", "descricao")
    @classmethod
    def sanitize_fields(cls, value: Optional[str]):
        if value is None:
            return value
        return Text.sanitize_input(value)

    @field_validator("apontamento_pag_posterior", "custas_na_confirmacao")
    @classmethod
    def validate_sim_nao_fields(cls, value: Optional[str]):
        if value is None:
            return value
        return normalize_sim_nao(value)

    @field_validator("layout_id", mode="before")
    @classmethod
    def validate_layout_id(cls, value):
        if value is None or value == "":
            return None
        try:
            layout_id = int(value)
        except (TypeError, ValueError) as exc:
            raise ValueError("O layout_id deve ser um número inteiro.") from exc
        if layout_id <= 0:
            raise ValueError("O layout_id deve ser maior que zero.")
        return layout_id
