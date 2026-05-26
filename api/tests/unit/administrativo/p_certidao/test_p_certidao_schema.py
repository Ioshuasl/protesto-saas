import pytest
from pydantic import ValidationError

from packages.v1.administrativo.schemas.p_certidao_schema import (
    PCertidaoIndexSchema,
    PCertidaoSaveSchema,
    normalize_status,
    normalize_tipo_certidao,
    normalize_tipo_certidao_index,
    normalize_tipo_remessa,
)


@pytest.mark.unit
def test_index_schema_accepts_expected_filters():
    schema = PCertidaoIndexSchema(
        tipo_certidao="p",
        data_certidao="2026-05-26",
        data_inicio="2026-05-01",
        data_fim="2026-05-31",
        status="a",
        busca="  maria  ",
    )

    assert schema.tipo_certidao == "P"
    assert str(schema.data_inicio) == "2026-05-01"
    assert str(schema.data_fim) == "2026-05-31"
    assert schema.status == "A"
    assert schema.busca == "maria"


@pytest.mark.unit
def test_index_schema_rejects_tipo_certidao_serasa():
    with pytest.raises(ValidationError):
        PCertidaoIndexSchema(tipo_certidao="R")


@pytest.mark.unit
def test_index_schema_rejects_unknown_filter():
    with pytest.raises(ValidationError):
        PCertidaoIndexSchema(tipo_certidao="P", apresentante="x")


@pytest.mark.unit
def test_save_schema_accepts_all_tipo_certidao_siglas():
    assert PCertidaoSaveSchema(tipo_certidao="R").tipo_certidao == "R"
    assert PCertidaoSaveSchema(tipo_certidao="P").tipo_certidao == "P"
    assert PCertidaoSaveSchema(tipo_certidao="N").tipo_certidao == "N"


@pytest.mark.unit
def test_sigla_normalizers_reject_invalid_values():
    with pytest.raises(ValueError):
        normalize_tipo_certidao("X")
    with pytest.raises(ValueError):
        normalize_tipo_certidao_index("R")
    with pytest.raises(ValueError):
        normalize_tipo_remessa("X")
    with pytest.raises(ValueError):
        normalize_status("I")
