from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Any, Mapping, Optional, Union

from pydantic import BaseModel, ConfigDict, field_validator, model_validator

from actions.validations.text import Text

# P_PESSOA — MICRO_EMPRESA VARCHAR(1): S = sim; N, NULL ou vazio = não
SIM_CODIGO = "S"
NAO_CODIGO = "N"
SIM_NAO_CODIGOS = frozenset({SIM_CODIGO, NAO_CODIGO})

# P_PESSOA — tipo inferido pelo documento (não há coluna TIPO_PESSOA no Firebird)
TIPO_PESSOA_FISICA = "F"
TIPO_PESSOA_JURIDICA = "J"
TIPO_PESSOA_CODIGOS = frozenset({TIPO_PESSOA_FISICA, TIPO_PESSOA_JURIDICA})
CPF_DIGITOS = 11
CNPJ_DIGITOS = 14

# P_PESSOA_VINCULO (domínio; CRUD de vínculo fora deste módulo)
TIPO_VINCULO_CODIGOS = frozenset({"APRESENTANTE", "CEDENTE", "CREDOR", "DEVEDOR"})
DEVEDOR_TIPO_ACEITE_CODIGOS = frozenset({"A", "E"})  # A = Aceite, E = Edital

_NUMERIC_ID_KEYS = frozenset(
    {
        "pessoa_id",
        "estado_civil_id",
        "profissao_id",
        "cidade_id",
        "chave_pessoa_imp",
    }
)


def normalize_sim_nao(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    normalized = str(value).strip().upper()
    if not normalized:
        return NAO_CODIGO
    if normalized not in SIM_NAO_CODIGOS:
        raise ValueError(f"Valor inválido: '{value}'. Use S (sim) ou N (não).")
    return normalized


def sim_nao_from_db(value: Optional[str]) -> str:
    if value is None or not str(value).strip():
        return NAO_CODIGO
    if str(value).strip().upper() == SIM_CODIGO:
        return SIM_CODIGO
    return NAO_CODIGO


def sim_nao_to_db(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    code = normalize_sim_nao(value)
    if code == SIM_CODIGO:
        return SIM_CODIGO
    return None


def normalize_tipo_vinculo(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    normalized = str(value).strip().upper()
    if not normalized:
        return None
    if normalized not in TIPO_VINCULO_CODIGOS:
        raise ValueError(
            f"Tipo de vínculo inválido: '{value}'. "
            f"Use: {', '.join(sorted(TIPO_VINCULO_CODIGOS))}."
        )
    return normalized


def normalize_devedor_tipo_aceite(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    normalized = str(value).strip().upper()
    if not normalized:
        return None
    if normalized not in DEVEDOR_TIPO_ACEITE_CODIGOS:
        raise ValueError(
            f"Tipo de aceite inválido: '{value}'. Use A (Aceite) ou E (Edital)."
        )
    return normalized


def sanitize_cpfcnpj(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    sanitized = Text.sanitize_input(str(value))
    digits = "".join(ch for ch in sanitized if ch.isdigit())
    return digits or None


def normalize_tipo_pessoa(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    normalized = str(value).strip().upper()
    if not normalized:
        return None
    if normalized not in TIPO_PESSOA_CODIGOS:
        raise ValueError(
            f"Tipo de pessoa inválido: '{value}'. "
            "Use F (pessoa física / CPF) ou J (pessoa jurídica / CNPJ)."
        )
    return normalized


def infer_tipo_pessoa_from_cpfcnpj(cpfcnpj: Optional[str]) -> Optional[str]:
    digits = sanitize_cpfcnpj(cpfcnpj)
    if not digits:
        return None
    if len(digits) == CPF_DIGITOS:
        return TIPO_PESSOA_FISICA
    if len(digits) == CNPJ_DIGITOS:
        return TIPO_PESSOA_JURIDICA
    return None


def validate_cpfcnpj_for_tipo(
    cpfcnpj: Optional[str], tipo_pessoa: str
) -> Optional[str]:
    tipo = normalize_tipo_pessoa(tipo_pessoa)
    if tipo is None:
        raise ValueError("Tipo de pessoa é obrigatório.")
    digits = sanitize_cpfcnpj(cpfcnpj)
    expected = CPF_DIGITOS if tipo == TIPO_PESSOA_FISICA else CNPJ_DIGITOS
    label = "CPF" if tipo == TIPO_PESSOA_FISICA else "CNPJ"
    if not digits:
        raise ValueError(f"{label} é obrigatório.")
    if len(digits) != expected:
        raise ValueError(f"{label} deve conter {expected} dígitos.")
    return digits


def map_pessoa_row(row: Optional[Mapping[str, Any]]) -> Optional[dict[str, Any]]:
    if row is None:
        return None

    mapped: dict[str, Any] = {}
    for key, value in dict(row).items():
        mapped[str(key).lower()] = value

    for key in _NUMERIC_ID_KEYS:
        val = mapped.get(key)
        if isinstance(val, Decimal):
            mapped[key] = int(val)

    for key, value in list(mapped.items()):
        if value is not None and isinstance(value, str):
            stripped = value.strip()
            mapped[key] = stripped if stripped else None

    if "micro_empresa" in mapped:
        mapped["micro_empresa"] = sim_nao_from_db(mapped.get("micro_empresa"))

    mapped["tipo_pessoa"] = infer_tipo_pessoa_from_cpfcnpj(mapped.get("cpfcnpj"))

    return mapped


class PPessoaSchema(BaseModel):
    pessoa_id: Optional[int] = None
    nome: Optional[str] = None
    cpfcnpj: Optional[str] = None
    endereco: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    uf: Optional[str] = None
    cep: Optional[str] = None
    telefone: Optional[str] = None
    rg: Optional[str] = None
    observacoes: Optional[str] = None
    banco: Optional[str] = None
    agencia: Optional[str] = None
    conta: Optional[str] = None
    nome_banco: Optional[str] = None
    nacionalidade: Optional[str] = None
    estado_civil_id: Optional[int] = None
    profissao_id: Optional[int] = None
    cidade_agencia: Optional[str] = None
    data_nascimento: Optional[Union[datetime, date]] = None
    email: Optional[str] = None
    cidade_id: Optional[int] = None
    data_validade: Optional[Union[datetime, date]] = None
    micro_empresa: Optional[str] = None
    chave_pessoa_imp: Optional[int] = None
    cod_cra: Optional[str] = None
    nome_fantasia: Optional[str] = None
    total_titulos: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class PPessoaIdSchema(BaseModel):
    pessoa_id: int


class PPessoaCpfcnpjSchema(BaseModel):
    cpfcnpj: str
    pessoa_id: Optional[int] = None

    @field_validator("cpfcnpj", mode="after")
    @classmethod
    def validate_cpfcnpj(cls, value: str):
        digits = sanitize_cpfcnpj(value)
        if not digits:
            raise ValueError("CPF/CNPJ inválido.")
        return digits


class PPessoaIndexSchema(BaseModel):
    """busca: termo único pesquisado em NOME, CPFCNPJ e TELEFONE (resultados concatenados)."""

    busca: Optional[str] = None
    cidade: Optional[str] = None
    uf: Optional[str] = None
    tipo_pessoa: Optional[str] = None

    model_config = ConfigDict(extra="forbid")

    @field_validator("busca", "cidade", mode="before")
    @classmethod
    def sanitize_text_filters(cls, value):
        if value is None or value == "":
            return None
        return Text.sanitize_input(str(value))

    @field_validator("uf", mode="before")
    @classmethod
    def sanitize_uf_filter(cls, value):
        if value is None or value == "":
            return None
        return Text.sanitize_input(str(value)).upper()

    @field_validator("tipo_pessoa", mode="before")
    @classmethod
    def sanitize_tipo_pessoa_filter(cls, value):
        if value is None or value == "":
            return None
        return normalize_tipo_pessoa(str(value))


class PPessoaSaveSchema(BaseModel):
    pessoa_id: Optional[int] = None
    nome: str
    tipo_pessoa: str
    cpfcnpj: Optional[str] = None
    endereco: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    uf: Optional[str] = None
    cep: Optional[str] = None
    telefone: Optional[str] = None
    rg: Optional[str] = None
    observacoes: Optional[str] = None
    banco: Optional[str] = None
    agencia: Optional[str] = None
    conta: Optional[str] = None
    nome_banco: Optional[str] = None
    nacionalidade: Optional[str] = None
    estado_civil_id: Optional[int] = None
    profissao_id: Optional[int] = None
    cidade_agencia: Optional[str] = None
    data_nascimento: Optional[Union[datetime, date]] = None
    email: Optional[str] = None
    cidade_id: Optional[int] = None
    data_validade: Optional[Union[datetime, date]] = None
    micro_empresa: Optional[str] = NAO_CODIGO
    chave_pessoa_imp: Optional[int] = None
    cod_cra: Optional[str] = None
    nome_fantasia: Optional[str] = None

    @field_validator(
        "nome",
        "endereco",
        "bairro",
        "cidade",
        "cep",
        "telefone",
        "rg",
        "observacoes",
        "banco",
        "agencia",
        "conta",
        "nome_banco",
        "nacionalidade",
        "cidade_agencia",
        "email",
        "cod_cra",
        "nome_fantasia",
        mode="before",
    )
    @classmethod
    def sanitize_optional_text(cls, value):
        if value is None or value == "":
            return None
        return Text.sanitize_input(str(value))

    @field_validator("nome", mode="after")
    @classmethod
    def validate_nome(cls, value: str):
        if not value or not value.strip():
            raise ValueError("O nome é obrigatório.")
        return value.strip()

    @field_validator("cpfcnpj", mode="before")
    @classmethod
    def sanitize_document(cls, value):
        if value is None or value == "":
            return None
        return sanitize_cpfcnpj(str(value))

    @field_validator("uf", mode="before")
    @classmethod
    def sanitize_uf(cls, value):
        if value is None or value == "":
            return None
        normalized = Text.sanitize_input(str(value)).upper()
        return normalized[:3] if normalized else None

    @field_validator("micro_empresa", mode="after")
    @classmethod
    def validate_micro_empresa(cls, value: Optional[str]):
        if value is None:
            return NAO_CODIGO
        return normalize_sim_nao(value)

    @field_validator("tipo_pessoa", mode="before")
    @classmethod
    def sanitize_tipo_pessoa(cls, value):
        return normalize_tipo_pessoa(str(value))

    @model_validator(mode="after")
    def validate_document_and_dates(self):
        self.cpfcnpj = validate_cpfcnpj_for_tipo(self.cpfcnpj, self.tipo_pessoa)
        if self.data_nascimento is not None:
            self.data_nascimento = _to_naive_datetime(self.data_nascimento)
        if self.data_validade is not None:
            self.data_validade = _to_naive_datetime(self.data_validade)
        return self


class PPessoaUpdateSchema(BaseModel):
    nome: Optional[str] = None
    tipo_pessoa: Optional[str] = None
    cpfcnpj: Optional[str] = None
    endereco: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    uf: Optional[str] = None
    cep: Optional[str] = None
    telefone: Optional[str] = None
    rg: Optional[str] = None
    observacoes: Optional[str] = None
    banco: Optional[str] = None
    agencia: Optional[str] = None
    conta: Optional[str] = None
    nome_banco: Optional[str] = None
    nacionalidade: Optional[str] = None
    estado_civil_id: Optional[int] = None
    profissao_id: Optional[int] = None
    cidade_agencia: Optional[str] = None
    data_nascimento: Optional[Union[datetime, date]] = None
    email: Optional[str] = None
    cidade_id: Optional[int] = None
    data_validade: Optional[Union[datetime, date]] = None
    micro_empresa: Optional[str] = None
    chave_pessoa_imp: Optional[int] = None
    cod_cra: Optional[str] = None
    nome_fantasia: Optional[str] = None

    @field_validator(
        "nome",
        "endereco",
        "bairro",
        "cidade",
        "cep",
        "telefone",
        "rg",
        "observacoes",
        "banco",
        "agencia",
        "conta",
        "nome_banco",
        "nacionalidade",
        "cidade_agencia",
        "email",
        "cod_cra",
        "nome_fantasia",
        mode="before",
    )
    @classmethod
    def sanitize_optional_text(cls, value):
        if value is None:
            return value
        if value == "":
            return None
        return Text.sanitize_input(str(value))

    @field_validator("cpfcnpj", mode="before")
    @classmethod
    def sanitize_document(cls, value):
        if value is None:
            return value
        if value == "":
            return None
        return sanitize_cpfcnpj(str(value))

    @field_validator("uf", mode="before")
    @classmethod
    def sanitize_uf(cls, value):
        if value is None:
            return value
        if value == "":
            return None
        return Text.sanitize_input(str(value)).upper()[:3]

    @field_validator("micro_empresa", mode="after")
    @classmethod
    def validate_micro_empresa(cls, value: Optional[str]):
        if value is None:
            return value
        return normalize_sim_nao(value)

    @field_validator("tipo_pessoa", mode="before")
    @classmethod
    def sanitize_tipo_pessoa(cls, value):
        if value is None or value == "":
            return None
        return normalize_tipo_pessoa(str(value))

    @model_validator(mode="after")
    def validate_document_and_dates(self):
        if self.cpfcnpj is not None:
            tipo = self.tipo_pessoa or infer_tipo_pessoa_from_cpfcnpj(self.cpfcnpj)
            if tipo is None:
                raise ValueError(
                    "Informe tipo_pessoa (F ou J) ou um CPF/CNPJ com 11 ou 14 dígitos."
                )
            self.cpfcnpj = validate_cpfcnpj_for_tipo(self.cpfcnpj, tipo)
        elif self.tipo_pessoa is not None:
            raise ValueError("Informe o CPF/CNPJ ao alterar o tipo de pessoa.")
        if self.data_nascimento is not None:
            self.data_nascimento = _to_naive_datetime(self.data_nascimento)
        if self.data_validade is not None:
            self.data_validade = _to_naive_datetime(self.data_validade)
        return self


def _to_naive_datetime(value: Union[datetime, date]) -> datetime:
    if isinstance(value, datetime):
        return value.replace(tzinfo=None) if value.tzinfo else value
    return datetime.combine(value, datetime.min.time())
