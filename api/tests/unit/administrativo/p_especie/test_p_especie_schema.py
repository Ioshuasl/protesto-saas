import pytest

from packages.v1.administrativo.schemas.p_especie_schema import (
    PEspecieSaveSchema,
    normalize_especie,
)


@pytest.mark.unit
def test_normalize_especie_uppercases_and_trims():
    assert normalize_especie("  dmi  ") == "DMI"


@pytest.mark.unit
def test_normalize_especie_rejects_long_sigla():
    with pytest.raises(ValueError, match="máximo 3"):
        normalize_especie("ABCD")


@pytest.mark.unit
def test_save_schema_normalizes_especie():
    schema = PEspecieSaveSchema(especie="ch", descricao="Cheque")
    assert schema.especie == "CH"
    assert schema.descricao == "Cheque"
