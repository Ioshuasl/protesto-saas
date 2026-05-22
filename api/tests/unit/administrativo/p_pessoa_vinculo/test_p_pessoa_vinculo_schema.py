import pytest

from packages.v1.administrativo.schemas.p_pessoa_schema import normalize_tipo_vinculo
from packages.v1.administrativo.schemas.p_pessoa_vinculo_schema import (
    PPessoaVinculoSaveSchema,
    build_db_payload_from_schema,
    map_pessoa_vinculo_row,
)


@pytest.mark.unit
def test_normalize_tipo_vinculo_devedor():
    assert normalize_tipo_vinculo("devedor") == "DEVEDOR"


@pytest.mark.unit
def test_map_pessoa_vinculo_row_hides_principal_favorecido():
    row = {
        "PESSOA_VINCULO_ID": 1,
        "TIPO_VINCULO": "DEVEDOR",
        "GERAR_SELO": "S",
        "PRINCIPAL": "S",
        "FAVORECIDO": "N",
    }
    mapped = map_pessoa_vinculo_row(row)
    assert mapped is not None
    assert "principal" not in mapped
    assert "favorecido" not in mapped
    assert mapped["gerar_selo"] == "S"
    assert mapped["tipo_vinculo"] == "DEVEDOR"


@pytest.mark.unit
def test_build_db_payload_sim_nao_to_db():
    payload = build_db_payload_from_schema({"gerar_selo": "N"})
    assert payload["GERAR_SELO"] is None


@pytest.mark.unit
def test_save_schema_requires_titulo_and_tipo():
    schema = PPessoaVinculoSaveSchema(titulo_id=10, tipo_vinculo="CREDOR")
    assert schema.titulo_id == 10
    assert schema.tipo_vinculo == "CREDOR"


@pytest.mark.unit
def test_save_schema_rejects_invalid_tipo():
    with pytest.raises(ValueError, match="Tipo de vínculo"):
        PPessoaVinculoSaveSchema(titulo_id=1, tipo_vinculo="INVALIDO")
