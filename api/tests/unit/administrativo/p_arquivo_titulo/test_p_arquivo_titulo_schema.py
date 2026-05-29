import ast
import zlib
from datetime import date

import pytest

from packages.v1.administrativo.schemas.p_arquivo_titulo_schema import (
    PArquivoTituloIndexSchema,
    PArquivoTituloShowSchema,
    api_money_to_db,
    db_money_to_api,
    decode_blob_conteudo,
    encode_arquivo_download_content,
    map_arquivo_titulo_row,
    map_titulos_numero_apontamento_list,
    parse_arquivo_titulo_includes,
    sanitize_arquivo_download_filename,
)


@pytest.mark.unit
def test_index_schema_portador_codigo_uppercase():
    schema = PArquivoTituloIndexSchema(portador_codigo="756")
    assert schema.portador_codigo == "756"


@pytest.mark.unit
def test_index_schema_date_range_filters():
    schema = PArquivoTituloIndexSchema(
        data_inicio=date(2025, 1, 1),
        data_fim=date(2025, 1, 31),
    )
    assert schema.data_inicio == date(2025, 1, 1)
    assert schema.data_fim == date(2025, 1, 31)


@pytest.mark.unit
def test_api_money_to_db_and_back():
    assert api_money_to_db(1171.23) == 117123
    assert db_money_to_api(117123) == 1171.23


@pytest.mark.unit
def test_map_arquivo_titulo_row_excludes_blobs():
    from decimal import Decimal

    row = {
        "ARQUIVO_TITULO_ID": Decimal("302735"),
        "SOMA_VLR_REMESSA": Decimal("117123"),
        "NOME_ARQUIVO": "B7562210.251",
        "TEXTO": b"conteudo",
        "TEXTO_IMPORTADO": b"importado",
    }
    mapped = map_arquivo_titulo_row(row)
    assert mapped is not None
    assert mapped["arquivo_titulo_id"] == 302735
    assert mapped["soma_vlr_remessa"] == 1171.23
    assert "texto" not in mapped
    assert "texto_importado" not in mapped


@pytest.mark.unit
def test_decode_blob_conteudo_plain_bytes():
    payload = "Febraban".encode("latin-1")
    assert decode_blob_conteudo(payload) == "Febraban"


@pytest.mark.unit
def test_decode_blob_conteudo_zlib_from_orm_repr_string():
    plain = "0756BANCO COOPERATIVO DO BRASIL S.A.        "
    compressed = zlib.compress(plain.encode("iso-8859-1"))
    orm_repr = repr(compressed)
    decoded = decode_blob_conteudo(orm_repr)
    assert decoded is not None
    assert decoded.endswith("        ")
    assert plain.rstrip() in decoded


@pytest.mark.unit
def test_parse_arquivo_titulo_includes():
    assert parse_arquivo_titulo_includes(None) == frozenset()
    assert parse_arquivo_titulo_includes("") == frozenset()
    assert parse_arquivo_titulo_includes("titulos") == frozenset({"titulos"})
    assert parse_arquivo_titulo_includes(" Titulos , invalid ") == frozenset(
        {"titulos", "invalid"}
    )


@pytest.mark.unit
def test_map_titulos_numero_apontamento_list():
    from decimal import Decimal

    mapped = map_titulos_numero_apontamento_list(
        [
            {"NUMERO_APONTAMENTO": Decimal("12345")},
            {"NUMERO_APONTAMENTO": None},
        ]
    )
    assert mapped == [
        {"numero_apontamento": 12345},
        {"numero_apontamento": None},
    ]


@pytest.mark.unit
def test_index_schema_with_includes():
    schema = PArquivoTituloIndexSchema(includes=frozenset({"titulos"}))
    assert schema.includes == frozenset({"titulos"})


@pytest.mark.unit
def test_show_schema_from_id_with_include():
    schema = PArquivoTituloShowSchema.from_id(300821, include="titulos")
    assert schema.arquivo_titulo_id == 300821
    assert schema.includes == frozenset({"titulos"})


@pytest.mark.unit
def test_sanitize_arquivo_download_filename():
    assert sanitize_arquivo_download_filename("B7562210.251", 1) == "B7562210.251"
    assert sanitize_arquivo_download_filename("path/evil.rem", 2) == "pathevil.rem"
    assert sanitize_arquivo_download_filename(None, 99) == "arquivo_titulo_99.rem"


@pytest.mark.unit
def test_encode_arquivo_download_content_iso8859():
    payload = "linha com acentuação ç".encode("iso-8859-1")
    assert encode_arquivo_download_content("linha com acentuação ç") == payload


@pytest.mark.unit
def test_decode_blob_conteudo_preserves_trailing_spaces():
    payload = "linha com espacos      ".encode("latin-1")
    assert decode_blob_conteudo(payload) == "linha com espacos      "
