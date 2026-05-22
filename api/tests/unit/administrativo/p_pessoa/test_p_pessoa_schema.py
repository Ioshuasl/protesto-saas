import pytest

from packages.v1.administrativo.schemas.p_pessoa_schema import (
    PPessoaIndexSchema,
    PPessoaSaveSchema,
    infer_tipo_pessoa_from_cpfcnpj,
    normalize_devedor_tipo_aceite,
    normalize_sim_nao,
    normalize_tipo_pessoa,
    normalize_tipo_vinculo,
    sim_nao_from_db,
    sim_nao_to_db,
    validate_cpfcnpj_for_tipo,
)


@pytest.mark.unit
def test_sim_nao_from_db():
    assert sim_nao_from_db("S") == "S"
    assert sim_nao_from_db("N") == "N"
    assert sim_nao_from_db(None) == "N"
    assert sim_nao_from_db("") == "N"


@pytest.mark.unit
def test_sim_nao_to_db():
    assert sim_nao_to_db("S") == "S"
    assert sim_nao_to_db("N") is None
    assert sim_nao_to_db(None) is None


@pytest.mark.unit
def test_normalize_tipo_vinculo():
    assert normalize_tipo_vinculo("devedor") == "DEVEDOR"
    with pytest.raises(ValueError):
        normalize_tipo_vinculo("INVALIDO")


@pytest.mark.unit
def test_normalize_devedor_tipo_aceite():
    assert normalize_devedor_tipo_aceite("a") == "A"
    assert normalize_devedor_tipo_aceite("E") == "E"
    with pytest.raises(ValueError):
        normalize_devedor_tipo_aceite("X")


@pytest.mark.unit
def test_normalize_tipo_pessoa():
    assert normalize_tipo_pessoa("f") == "F"
    assert normalize_tipo_pessoa("J") == "J"
    with pytest.raises(ValueError):
        normalize_tipo_pessoa("X")


@pytest.mark.unit
def test_infer_tipo_pessoa_from_cpfcnpj():
    assert infer_tipo_pessoa_from_cpfcnpj("123.456.789-01") == "F"
    assert infer_tipo_pessoa_from_cpfcnpj("07158428000106") == "J"
    assert infer_tipo_pessoa_from_cpfcnpj(None) is None


@pytest.mark.unit
def test_validate_cpfcnpj_for_tipo():
    assert validate_cpfcnpj_for_tipo("12345678901", "F") == "12345678901"
    assert validate_cpfcnpj_for_tipo("07158428000106", "J") == "07158428000106"
    with pytest.raises(ValueError):
        validate_cpfcnpj_for_tipo("123", "F")
    with pytest.raises(ValueError):
        validate_cpfcnpj_for_tipo("12345678901", "J")


@pytest.mark.unit
def test_ppessoa_index_schema_tipo_pessoa():
    schema = PPessoaIndexSchema(tipo_pessoa="f")
    assert schema.tipo_pessoa == "F"


@pytest.mark.unit
def test_ppessoa_save_schema_tipo_e_documento():
    schema = PPessoaSaveSchema(
        nome="Teste",
        tipo_pessoa="J",
        cpfcnpj="07.158.428/0001-06",
    )
    assert schema.cpfcnpj == "07158428000106"
