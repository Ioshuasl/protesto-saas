import pytest

from packages.v1.administrativo.schemas.p_motivos_schema import (
    normalize_situacao,
    situacao_from_db,
    situacao_to_db,
)


@pytest.mark.unit
def test_situacao_to_db_ativo():
    assert situacao_to_db("A") == "A"


@pytest.mark.unit
def test_situacao_to_db_inativo_grava_null():
    assert situacao_to_db("I") is None


@pytest.mark.unit
def test_situacao_from_db_null_e_inativo():
    assert situacao_from_db(None) == "I"
    assert situacao_from_db("") == "I"
    assert situacao_from_db("I") == "I"


@pytest.mark.unit
def test_situacao_from_db_ativo():
    assert situacao_from_db("A") == "A"


@pytest.mark.unit
def test_normalize_situacao_rejeita_invalido():
    with pytest.raises(ValueError):
        normalize_situacao("X")
