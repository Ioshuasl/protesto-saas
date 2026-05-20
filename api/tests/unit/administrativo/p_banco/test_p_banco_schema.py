import pytest

from packages.v1.administrativo.schemas.p_banco_schema import (
    NAO_CODIGO,
    SIM_CODIGO,
    PBancoSaveSchema,
    normalize_sim_nao,
    normalize_sim_nao_from_db,
)


@pytest.mark.unit
@pytest.mark.parametrize(
    "value,expected",
    [
        ("s", SIM_CODIGO),
        ("N", NAO_CODIGO),
        (None, None),
    ],
)
def test_normalize_sim_nao(value, expected):
    assert normalize_sim_nao(value) == expected


@pytest.mark.unit
@pytest.mark.parametrize(
    "value,expected",
    [
        (None, NAO_CODIGO),
        ("", NAO_CODIGO),
        ("S", SIM_CODIGO),
        ("x", NAO_CODIGO),
    ],
)
def test_normalize_sim_nao_from_db(value, expected):
    assert normalize_sim_nao_from_db(value) == expected


@pytest.mark.unit
def test_save_schema_rejects_invalid_sim_nao():
    with pytest.raises(ValueError):
        PBancoSaveSchema(
            codigo_banco="TST",
            descricao="Teste",
            layout_id=25,
            apontamento_pag_posterior="X",
            custas_na_confirmacao="N",
        )
