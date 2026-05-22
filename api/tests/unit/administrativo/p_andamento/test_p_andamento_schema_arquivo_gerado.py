import pytest

from packages.v1.administrativo.schemas.p_andamento_schema import (
    ARQUIVO_GERADO_AGUARDANDO,
    ARQUIVO_GERADO_EXPORTADO,
    arquivo_gerado_from_db,
    normalize_arquivo_gerado,
)


@pytest.mark.unit
def test_normalize_arquivo_gerado_aguardando():
    assert normalize_arquivo_gerado("d") == ARQUIVO_GERADO_AGUARDANDO


@pytest.mark.unit
def test_normalize_arquivo_gerado_exportado():
    assert normalize_arquivo_gerado("E") == ARQUIVO_GERADO_EXPORTADO


@pytest.mark.unit
def test_arquivo_gerado_from_db():
    assert arquivo_gerado_from_db("D") == ARQUIVO_GERADO_AGUARDANDO
    assert arquivo_gerado_from_db("e") == ARQUIVO_GERADO_EXPORTADO


@pytest.mark.unit
def test_normalize_arquivo_gerado_rejeita_invalido():
    with pytest.raises(ValueError):
        normalize_arquivo_gerado("X")
