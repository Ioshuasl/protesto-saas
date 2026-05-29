from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Any, Mapping, Optional

from pydantic import BaseModel, ConfigDict, field_validator

from actions.data.binary_blob_codec import BinaryBlobCodec
from actions.validations.text import Text
from database.orm_firebird import normalize_row_keys


def _sanitize_optional_text(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    sanitized = Text.sanitize_input(str(value)).strip()
    return sanitized or None


def api_money_to_db(value: Optional[float]) -> Optional[int]:
    if value is None:
        return None
    return int(round(float(value) * 100))


def db_money_to_api(value: Any) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, Decimal):
        return float(value) / 100
    return float(value) / 100


def decode_blob_conteudo(value: Any) -> Optional[str]:
    """Decodifica TEXTO / TEXTO_IMPORTADO (BLOB SUB_TYPE BINARY + zlib Febraban)."""
    return BinaryBlobCodec.to_text(value)


def sanitize_arquivo_download_filename(
    nome_arquivo: Optional[str],
    arquivo_titulo_id: int,
) -> str:
    """Nome seguro para Content-Disposition (coluna NOME_ARQUIVO)."""
    if nome_arquivo is not None:
        cleaned = str(nome_arquivo).strip().replace("\\", "").replace("/", "")
        if cleaned:
            return cleaned
    return f"arquivo_titulo_{arquivo_titulo_id}.rem"


def encode_arquivo_download_content(conteudo: str) -> bytes:
    """Bytes do arquivo CRA (Febraban em ISO-8859-1)."""
    return conteudo.encode("iso-8859-1")


class PArquivoTituloIdSchema(BaseModel):
    arquivo_titulo_id: int


def parse_arquivo_titulo_includes(include: Optional[str]) -> frozenset[str]:
    if include is None or not str(include).strip():
        return frozenset()
    return frozenset(
        part.strip().lower() for part in str(include).split(",") if part.strip()
    )


class PArquivoTituloShowSchema(BaseModel):
    arquivo_titulo_id: int
    includes: frozenset[str] = frozenset()

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @classmethod
    def from_id(
        cls,
        arquivo_titulo_id: int,
        include: Optional[str] = None,
    ) -> "PArquivoTituloShowSchema":
        return cls(
            arquivo_titulo_id=arquivo_titulo_id,
            includes=parse_arquivo_titulo_includes(include),
        )


def map_titulos_numero_apontamento_list(rows: Any) -> list[dict[str, Any]]:
    """Lista enxuta de títulos vinculados (somente numero_apontamento)."""
    if not isinstance(rows, list):
        return []

    mapped: list[dict[str, Any]] = []
    for item in rows:
        row = normalize_row_keys(item)
        if row is None:
            continue

        numero = row.get("numero_apontamento")
        if isinstance(numero, Decimal):
            numero = int(numero)
        elif numero is not None and str(numero).strip().isdigit():
            numero = int(str(numero).strip())

        mapped.append({"numero_apontamento": numero})

    return mapped


# Alias legado (show/index)
parse_arquivo_titulo_show_includes = parse_arquivo_titulo_includes


class PArquivoTituloIndexSchema(BaseModel):
    nome_arquivo: Optional[str] = None
    portador_codigo: Optional[str] = None
    codigo_praca: Optional[str] = None
    data_inicio: Optional[date] = None
    data_fim: Optional[date] = None
    includes: frozenset[str] = frozenset()

    model_config = ConfigDict(extra="forbid")

    @field_validator("nome_arquivo", "codigo_praca", mode="before")
    @classmethod
    def sanitize_text_filters(cls, value: Optional[str]) -> Optional[str]:
        return _sanitize_optional_text(value)

    @field_validator("portador_codigo", mode="before")
    @classmethod
    def sanitize_portador_codigo(cls, value: Optional[str]) -> Optional[str]:
        sanitized = _sanitize_optional_text(value)
        if sanitized is None:
            return None
        return sanitized.upper()


class PArquivoTituloSaveSchema(BaseModel):
    arquivo_titulo_id: Optional[int] = None
    data_importacao: Optional[datetime] = None
    quantidade: Optional[float] = None
    data_movimento: Optional[str] = None
    numero_sequencial: Optional[str] = None
    qtde_registros: Optional[str] = None
    qtde_titulos: Optional[str] = None
    qtde_indicacoes: Optional[str] = None
    qtde_originais: Optional[str] = None
    soma_vlr_remessa: Optional[float] = None
    soma_qtde_remessa: Optional[float] = None
    agencia_centralizadora: Optional[str] = None
    codigo_praca: Optional[str] = None
    sequencial_header: Optional[str] = None
    nome_arquivo: Optional[str] = None
    portador_nome: Optional[str] = None
    complemento_header: Optional[str] = None
    identificacao_registro: Optional[str] = None
    portador_codigo: Optional[str] = None
    id_transacao_remetente: Optional[str] = None
    id_transacao_destinatario: Optional[str] = None
    id_transacao_tipo: Optional[str] = None
    versao_layout: Optional[str] = None
    sequencial_footer: Optional[str] = None
    complemento_registro: Optional[str] = None

    model_config = ConfigDict(extra="forbid")

    @field_validator(
        "data_movimento",
        "numero_sequencial",
        "qtde_registros",
        "qtde_titulos",
        "qtde_indicacoes",
        "qtde_originais",
        "agencia_centralizadora",
        "codigo_praca",
        "sequencial_header",
        "nome_arquivo",
        "portador_nome",
        "complemento_header",
        "identificacao_registro",
        "portador_codigo",
        "id_transacao_remetente",
        "id_transacao_destinatario",
        "id_transacao_tipo",
        "versao_layout",
        "sequencial_footer",
        "complemento_registro",
        mode="before",
    )
    @classmethod
    def sanitize_optional_strings(cls, value: Optional[str]) -> Optional[str]:
        return _sanitize_optional_text(value)


class PArquivoTituloUpdateSchema(BaseModel):
    data_importacao: Optional[datetime] = None
    quantidade: Optional[float] = None
    data_movimento: Optional[str] = None
    numero_sequencial: Optional[str] = None
    qtde_registros: Optional[str] = None
    qtde_titulos: Optional[str] = None
    qtde_indicacoes: Optional[str] = None
    qtde_originais: Optional[str] = None
    soma_vlr_remessa: Optional[float] = None
    soma_qtde_remessa: Optional[float] = None
    agencia_centralizadora: Optional[str] = None
    codigo_praca: Optional[str] = None
    sequencial_header: Optional[str] = None
    nome_arquivo: Optional[str] = None
    portador_nome: Optional[str] = None
    complemento_header: Optional[str] = None
    identificacao_registro: Optional[str] = None
    portador_codigo: Optional[str] = None
    id_transacao_remetente: Optional[str] = None
    id_transacao_destinatario: Optional[str] = None
    id_transacao_tipo: Optional[str] = None
    versao_layout: Optional[str] = None
    sequencial_footer: Optional[str] = None
    complemento_registro: Optional[str] = None

    model_config = ConfigDict(extra="forbid")

    @field_validator(
        "data_movimento",
        "numero_sequencial",
        "qtde_registros",
        "qtde_titulos",
        "qtde_indicacoes",
        "qtde_originais",
        "agencia_centralizadora",
        "codigo_praca",
        "sequencial_header",
        "nome_arquivo",
        "portador_nome",
        "complemento_header",
        "identificacao_registro",
        "portador_codigo",
        "id_transacao_remetente",
        "id_transacao_destinatario",
        "id_transacao_tipo",
        "versao_layout",
        "sequencial_footer",
        "complemento_registro",
        mode="before",
    )
    @classmethod
    def sanitize_optional_strings(cls, value: Optional[str]) -> Optional[str]:
        return _sanitize_optional_text(value)


def map_arquivo_titulo_row(row: Optional[Mapping[str, Any]]) -> Optional[dict[str, Any]]:
    mapped = normalize_row_keys(row)
    if mapped is None:
        return None

    arquivo_id = mapped.get("arquivo_titulo_id")
    if isinstance(arquivo_id, Decimal):
        mapped["arquivo_titulo_id"] = int(arquivo_id)

    quantidade = mapped.get("quantidade")
    if isinstance(quantidade, Decimal):
        mapped["quantidade"] = float(quantidade)

    soma_qtde = mapped.get("soma_qtde_remessa")
    if isinstance(soma_qtde, Decimal):
        mapped["soma_qtde_remessa"] = float(soma_qtde)

    mapped["soma_vlr_remessa"] = db_money_to_api(mapped.get("soma_vlr_remessa"))

    for key in (
        "data_movimento",
        "numero_sequencial",
        "qtde_registros",
        "qtde_titulos",
        "qtde_indicacoes",
        "qtde_originais",
        "agencia_centralizadora",
        "codigo_praca",
        "sequencial_header",
        "nome_arquivo",
        "portador_nome",
        "complemento_header",
        "identificacao_registro",
        "portador_codigo",
        "id_transacao_remetente",
        "id_transacao_destinatario",
        "id_transacao_tipo",
        "versao_layout",
        "sequencial_footer",
        "complemento_registro",
    ):
        value = mapped.get(key)
        if value is not None:
            mapped[key] = str(value).strip() or None

    mapped.pop("texto", None)
    mapped.pop("texto_importado", None)

    return mapped
