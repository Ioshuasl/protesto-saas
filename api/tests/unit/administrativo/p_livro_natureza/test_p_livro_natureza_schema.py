import pytest

from packages.v1.administrativo.schemas.p_livro_natureza_schema import (
    PLivroNaturezaSaveSchema,
    normalize_sigla,
    normalize_situacao,
    situacao_from_db,
    situacao_to_db,
)


@pytest.mark.unit
def test_normalize_sigla_uppercases_and_trims():
    assert normalize_sigla("  ap  ") == "AP"


@pytest.mark.unit
def test_normalize_sigla_rejects_long_value():
    with pytest.raises(ValueError, match="máximo 3"):
        normalize_sigla("ABCD")


@pytest.mark.unit
def test_situacao_from_db_null_is_inativo():
    assert situacao_from_db(None) == "I"
    assert situacao_from_db("") == "I"


@pytest.mark.unit
def test_situacao_to_db_inativo_is_null():
    assert situacao_to_db("I") is None
    assert situacao_to_db("A") == "A"


@pytest.mark.unit
def test_save_schema_normalizes_fields():
    schema = PLivroNaturezaSaveSchema(
        sigla="pr", descricao="Protesto", situacao="a"
    )
    assert schema.sigla == "PR"
    assert schema.situacao == "A"
    assert normalize_situacao("I") == "I"
