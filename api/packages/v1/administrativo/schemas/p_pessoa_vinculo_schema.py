"""
Schemas e normalização de domínio para P_PESSOA_VINCULO.
PRINCIPAL e FAVORECIDO não são expostos na API (sempre vazios no banco).
"""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Any, Mapping, Optional, Union

from pydantic import BaseModel, ConfigDict, field_validator, model_validator

from actions.validations.text import Text
from packages.v1.administrativo.schemas.p_pessoa_schema import (
    DEVEDOR_TIPO_ACEITE_CODIGOS,
    TIPO_VINCULO_CODIGOS,
    normalize_devedor_tipo_aceite,
    normalize_sim_nao,
    normalize_tipo_vinculo,
    sanitize_cpfcnpj,
    sim_nao_from_db,
    sim_nao_to_db,
)

_NUMERIC_ID_KEYS = frozenset(
    {
        "pessoa_vinculo_id",
        "titulo_id",
        "pessoa_id",
        "estado_civil_id",
        "profissao_id",
        "ocorrencia_id",
        "chave_importacao",
        "ocorrencia_andamento_id",
        "controle_devedor",
    }
)

_VINCULO_FLAG_KEYS = frozenset({"gerar_selo", "devedor_microempresa"})

_HIDDEN_API_KEYS = frozenset({"principal", "favorecido"})

_SCHEMA_FIELD_TO_DB: dict[str, str] = {
    "nome": "NOME",
    "cpfcnpj": "CPFCNPJ",
    "endereco": "ENDERECO",
    "bairro": "BAIRRO",
    "cidade": "CIDADE",
    "uf": "UF",
    "cep": "CEP",
    "telefone": "TELEFONE",
    "rg": "RG",
    "titulo_id": "TITULO_ID",
    "tipo_vinculo": "TIPO_VINCULO",
    "pessoa_id": "PESSOA_ID",
    "banco": "BANCO",
    "agencia": "AGENCIA",
    "conta": "CONTA",
    "nome_banco": "NOME_BANCO",
    "nacionalidade": "NACIONALIDADE",
    "estado_civil_id": "ESTADO_CIVIL_ID",
    "profissao_id": "PROFISSAO_ID",
    "cidade_agencia": "CIDADE_AGENCIA",
    "gerar_selo": "GERAR_SELO",
    "devedor_data_aceite": "DEVEDOR_DATA_ACEITE",
    "devedor_agencia": "DEVEDOR_AGENCIA",
    "devedor_numero_ar": "DEVEDOR_NUMERO_AR",
    "devedor_recebido_por": "DEVEDOR_RECEBIDO_POR",
    "devedor_situacao": "DEVEDOR_SITUACAO",
    "devedor_tipo_aceite": "DEVEDOR_TIPO_ACEITE",
    "ocorrencia_id": "OCORRENCIA_ID",
    "chave_importacao": "CHAVE_IMPORTACAO",
    "devedor_microempresa": "DEVEDOR_MICROEMPRESA",
    "ocorrencia_andamento_id": "OCORRENCIA_ANDAMENTO_ID",
    "controle_devedor": "CONTROLE_DEVEDOR",
}


def map_pessoa_vinculo_row(row: Optional[Mapping[str, Any]]) -> Optional[dict[str, Any]]:
    if row is None:
        return None

    mapped: dict[str, Any] = {}
    for key, value in dict(row).items():
        lower = str(key).lower()
        if lower in _HIDDEN_API_KEYS:
            continue
        mapped[lower] = value

    for key in _NUMERIC_ID_KEYS:
        val = mapped.get(key)
        if isinstance(val, Decimal):
            mapped[key] = int(val)

    for key, value in list(mapped.items()):
        if value is not None and isinstance(value, str):
            stripped = value.strip()
            mapped[key] = stripped if stripped else None

    tipo = mapped.get("tipo_vinculo")
    if tipo is not None:
        mapped["tipo_vinculo"] = normalize_tipo_vinculo(tipo)

    for flag_key in _VINCULO_FLAG_KEYS:
        if flag_key in mapped:
            mapped[flag_key] = sim_nao_from_db(mapped.get(flag_key))

    aceite = mapped.get("devedor_tipo_aceite")
    if aceite is not None:
        mapped["devedor_tipo_aceite"] = normalize_devedor_tipo_aceite(aceite)

    pessoa = mapped.pop("pessoa", None)
    if isinstance(pessoa, Mapping):
        from database.orm_firebird import normalize_row_keys

        nested = normalize_row_keys(pessoa) or {}
        pid = nested.get("pessoa_id")
        if isinstance(pid, Decimal):
            nested["pessoa_id"] = int(pid)
        mapped["pessoa"] = nested

    titulo = mapped.pop("titulo", None)
    if isinstance(titulo, Mapping):
        from database.orm_firebird import normalize_row_keys

        nested = normalize_row_keys(titulo) or {}
        tid = nested.get("titulo_id")
        if isinstance(tid, Decimal):
            nested["titulo_id"] = int(tid)
        mapped["titulo"] = nested

    return mapped


def build_db_payload_from_schema(
    schema_payload: Mapping[str, Any],
    *,
    include_pessoa_vinculo_id: bool = False,
    pessoa_vinculo_id: Optional[int] = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    if include_pessoa_vinculo_id and pessoa_vinculo_id is not None:
        payload["PESSOA_VINCULO_ID"] = pessoa_vinculo_id

    for api_key, column in _SCHEMA_FIELD_TO_DB.items():
        if api_key not in schema_payload:
            continue
        value = schema_payload[api_key]
        if api_key in _VINCULO_FLAG_KEYS:
            payload[column] = sim_nao_to_db(value)
        else:
            payload[column] = value

    return payload


class PPessoaVinculoSchema(BaseModel):
    pessoa_vinculo_id: Optional[int] = None
    nome: Optional[str] = None
    cpfcnpj: Optional[str] = None
    endereco: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    uf: Optional[str] = None
    cep: Optional[str] = None
    telefone: Optional[str] = None
    rg: Optional[str] = None
    titulo_id: Optional[int] = None
    tipo_vinculo: Optional[str] = None
    pessoa_id: Optional[int] = None
    banco: Optional[str] = None
    agencia: Optional[str] = None
    conta: Optional[str] = None
    nome_banco: Optional[str] = None
    nacionalidade: Optional[str] = None
    estado_civil_id: Optional[int] = None
    profissao_id: Optional[int] = None
    cidade_agencia: Optional[str] = None
    gerar_selo: Optional[str] = None
    devedor_data_aceite: Optional[Union[datetime, date]] = None
    devedor_agencia: Optional[str] = None
    devedor_numero_ar: Optional[str] = None
    devedor_recebido_por: Optional[str] = None
    devedor_situacao: Optional[str] = None
    devedor_tipo_aceite: Optional[str] = None
    ocorrencia_id: Optional[int] = None
    chave_importacao: Optional[int] = None
    devedor_microempresa: Optional[str] = None
    ocorrencia_andamento_id: Optional[int] = None
    controle_devedor: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class PPessoaVinculoIdSchema(BaseModel):
    pessoa_vinculo_id: int


class PPessoaVinculoIndexSchema(BaseModel):
    titulo_id: Optional[int] = None
    pessoa_id: Optional[int] = None
    tipo_vinculo: Optional[str] = None
    nome: Optional[str] = None
    cpfcnpj: Optional[str] = None
    busca: Optional[str] = None

    model_config = ConfigDict(extra="forbid")

    @field_validator("titulo_id", "pessoa_id", mode="before")
    @classmethod
    def parse_int_filters(cls, value):
        if value is None or value == "":
            return None
        try:
            return int(value)
        except (TypeError, ValueError) as exc:
            raise ValueError("Filtro numérico inválido.") from exc

    @field_validator(
        "tipo_vinculo",
        "nome",
        "cpfcnpj",
        "busca",
        mode="before",
    )
    @classmethod
    def sanitize_filters(cls, value):
        if value is None or value == "":
            return None
        return Text.sanitize_input(str(value))

    @field_validator("cpfcnpj", mode="after")
    @classmethod
    def normalize_cpfcnpj_filter(cls, value: Optional[str]):
        if value is None:
            return value
        return sanitize_cpfcnpj(value) or value

    @field_validator("tipo_vinculo", mode="after")
    @classmethod
    def validate_tipo_vinculo_filter(cls, value: Optional[str]):
        if value is None:
            return value
        return normalize_tipo_vinculo(value)


class PPessoaVinculoSaveSchema(BaseModel):
    pessoa_vinculo_id: Optional[int] = None
    titulo_id: int
    tipo_vinculo: str
    nome: Optional[str] = None
    cpfcnpj: Optional[str] = None
    endereco: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    uf: Optional[str] = None
    cep: Optional[str] = None
    telefone: Optional[str] = None
    rg: Optional[str] = None
    pessoa_id: Optional[int] = None
    banco: Optional[str] = None
    agencia: Optional[str] = None
    conta: Optional[str] = None
    nome_banco: Optional[str] = None
    nacionalidade: Optional[str] = None
    estado_civil_id: Optional[int] = None
    profissao_id: Optional[int] = None
    cidade_agencia: Optional[str] = None
    gerar_selo: Optional[str] = None
    devedor_data_aceite: Optional[Union[datetime, date]] = None
    devedor_agencia: Optional[str] = None
    devedor_numero_ar: Optional[str] = None
    devedor_recebido_por: Optional[str] = None
    devedor_situacao: Optional[str] = None
    devedor_tipo_aceite: Optional[str] = None
    ocorrencia_id: Optional[int] = None
    chave_importacao: Optional[int] = None
    devedor_microempresa: Optional[str] = None
    ocorrencia_andamento_id: Optional[int] = None
    controle_devedor: Optional[int] = None

    @field_validator(
        "nome",
        "endereco",
        "bairro",
        "cidade",
        "uf",
        "cep",
        "telefone",
        "rg",
        "banco",
        "agencia",
        "conta",
        "nome_banco",
        "nacionalidade",
        "cidade_agencia",
        "devedor_agencia",
        "devedor_numero_ar",
        "devedor_recebido_por",
        "devedor_situacao",
        mode="before",
    )
    @classmethod
    def sanitize_text_fields(cls, value):
        if value is None:
            return None
        if isinstance(value, str) and not value.strip():
            return None
        return Text.sanitize_input(str(value))

    @field_validator("cpfcnpj", mode="before")
    @classmethod
    def sanitize_cpfcnpj_field(cls, value):
        if value is None or (isinstance(value, str) and not value.strip()):
            return None
        return sanitize_cpfcnpj(str(value))

    @field_validator("tipo_vinculo", mode="after")
    @classmethod
    def validate_tipo_vinculo_field(cls, value: str):
        return normalize_tipo_vinculo(value)

    @field_validator("gerar_selo", "devedor_microempresa", mode="after")
    @classmethod
    def validate_sim_nao_fields(cls, value: Optional[str]):
        if value is None:
            return None
        return normalize_sim_nao(value)

    @field_validator("devedor_tipo_aceite", mode="after")
    @classmethod
    def validate_devedor_tipo_aceite_field(cls, value: Optional[str]):
        if value is None:
            return None
        return normalize_devedor_tipo_aceite(value)

    @model_validator(mode="after")
    def validate_required_fields(self):
        if not self.tipo_vinculo:
            raise ValueError("tipo_vinculo: O tipo de vínculo é obrigatório.")
        return self


class PPessoaVinculoUpdateSchema(BaseModel):
    titulo_id: Optional[int] = None
    tipo_vinculo: Optional[str] = None
    nome: Optional[str] = None
    cpfcnpj: Optional[str] = None
    endereco: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    uf: Optional[str] = None
    cep: Optional[str] = None
    telefone: Optional[str] = None
    rg: Optional[str] = None
    pessoa_id: Optional[int] = None
    banco: Optional[str] = None
    agencia: Optional[str] = None
    conta: Optional[str] = None
    nome_banco: Optional[str] = None
    nacionalidade: Optional[str] = None
    estado_civil_id: Optional[int] = None
    profissao_id: Optional[int] = None
    cidade_agencia: Optional[str] = None
    gerar_selo: Optional[str] = None
    devedor_data_aceite: Optional[Union[datetime, date]] = None
    devedor_agencia: Optional[str] = None
    devedor_numero_ar: Optional[str] = None
    devedor_recebido_por: Optional[str] = None
    devedor_situacao: Optional[str] = None
    devedor_tipo_aceite: Optional[str] = None
    ocorrencia_id: Optional[int] = None
    chave_importacao: Optional[int] = None
    devedor_microempresa: Optional[str] = None
    ocorrencia_andamento_id: Optional[int] = None
    controle_devedor: Optional[int] = None

    @field_validator(
        "nome",
        "endereco",
        "bairro",
        "cidade",
        "uf",
        "cep",
        "telefone",
        "rg",
        "banco",
        "agencia",
        "conta",
        "nome_banco",
        "nacionalidade",
        "cidade_agencia",
        "devedor_agencia",
        "devedor_numero_ar",
        "devedor_recebido_por",
        "devedor_situacao",
        mode="before",
    )
    @classmethod
    def sanitize_text_fields(cls, value):
        if value is None:
            return value
        if isinstance(value, str) and not value.strip():
            return None
        return Text.sanitize_input(str(value))

    @field_validator("cpfcnpj", mode="before")
    @classmethod
    def sanitize_cpfcnpj_field(cls, value):
        if value is None:
            return value
        if isinstance(value, str) and not value.strip():
            return None
        return sanitize_cpfcnpj(str(value))

    @field_validator("tipo_vinculo", mode="after")
    @classmethod
    def validate_tipo_vinculo_field(cls, value: Optional[str]):
        if value is None:
            return value
        return normalize_tipo_vinculo(value)

    @field_validator("gerar_selo", "devedor_microempresa", mode="after")
    @classmethod
    def validate_sim_nao_fields(cls, value: Optional[str]):
        if value is None:
            return value
        return normalize_sim_nao(value)

    @field_validator("devedor_tipo_aceite", mode="after")
    @classmethod
    def validate_devedor_tipo_aceite_field(cls, value: Optional[str]):
        if value is None:
            return value
        return normalize_devedor_tipo_aceite(value)


__all__ = [
    "DEVEDOR_TIPO_ACEITE_CODIGOS",
    "TIPO_VINCULO_CODIGOS",
    "PPessoaVinculoSchema",
    "PPessoaVinculoIdSchema",
    "PPessoaVinculoIndexSchema",
    "PPessoaVinculoSaveSchema",
    "PPessoaVinculoUpdateSchema",
    "build_db_payload_from_schema",
    "map_pessoa_vinculo_row",
]
