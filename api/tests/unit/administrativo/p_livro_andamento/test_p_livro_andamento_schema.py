from datetime import date, datetime

import pytest

from packages.v1.administrativo.schemas.p_livro_andamento_schema import (
    PLivroAndamentoIndexSchema,
    PLivroAndamentoSaveSchema,
    is_livro_aberto,
    normalize_aberto,
    normalize_sigla,
)


@pytest.mark.unit
def test_is_livro_aberto_when_data_fechamento_null():
    assert is_livro_aberto(None) is True
    assert is_livro_aberto("") is True


@pytest.mark.unit
def test_is_livro_aberto_when_data_fechamento_set():
    assert is_livro_aberto(datetime(2026, 1, 1)) is False


@pytest.mark.unit
def test_normalize_aberto_valid_codes():
    assert normalize_aberto("s") == "S"
    assert normalize_aberto("n") == "N"


@pytest.mark.unit
def test_normalize_aberto_rejects_invalid():
    with pytest.raises(ValueError, match="aberto inválido"):
        normalize_aberto("X")


@pytest.mark.unit
def test_index_schema_validates_aberto():
    schema = PLivroAndamentoIndexSchema(aberto="S", livro_natureza_id=1)
    assert schema.aberto == "S"


@pytest.mark.unit
def test_save_schema_parses_date_to_datetime():
    schema = PLivroAndamentoSaveSchema(
        livro_natureza_id=1,
        folha_atual=1,
        numero_livro=10,
        numero_folhas=100,
        data_abertura=date(2026, 5, 21),
    )
    assert isinstance(schema.data_abertura, datetime)
    assert schema.data_abertura.hour == 0


@pytest.mark.unit
def test_normalize_sigla_uppercases():
    assert normalize_sigla(" ap ") == "AP"
