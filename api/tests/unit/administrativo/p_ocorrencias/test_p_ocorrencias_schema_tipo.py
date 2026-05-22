import pytest
from pydantic import ValidationError

from packages.v1.administrativo.schemas.p_ocorrencias_schema import (
    POcorrenciasSaveSchema,
    POcorrenciasUpdateSchema,
    normalize_tipo,
    tipo_from_db,
    tipo_to_db,
)


@pytest.mark.unit
def test_normalize_tipo_accepts_valid_codes():
    assert normalize_tipo("cadastro") == "CADASTRO"
    assert normalize_tipo("desistência") == "DESISTENCIA"


@pytest.mark.unit
def test_normalize_tipo_allows_empty():
    assert normalize_tipo("") is None
    assert normalize_tipo(None) is None


@pytest.mark.unit
def test_normalize_tipo_rejects_unknown():
    with pytest.raises(ValueError, match="Tipo inválido"):
        normalize_tipo("PROTESTO")


@pytest.mark.unit
def test_tipo_from_db_preserves_legacy_values():
    assert tipo_from_db("CANC/PAGTO") == "CANC/PAGTO"
    assert tipo_from_db(None) is None


@pytest.mark.unit
def test_tipo_to_db_persists_canonical():
    assert tipo_to_db("PAGAMENTO") == "PAGAMENTO"
    assert tipo_to_db("") is None


@pytest.mark.unit
def test_save_schema_allows_empty_tipo():
    schema = POcorrenciasSaveSchema(
        codigo="99",
        descricao="Teste",
        tipo="",
    )
    assert schema.tipo is None


@pytest.mark.unit
def test_save_schema_rejects_invalid_tipo():
    with pytest.raises(ValidationError):
        POcorrenciasSaveSchema(
            codigo="99",
            descricao="Teste",
            tipo="LEGADO",
        )


@pytest.mark.unit
def test_update_schema_accepts_clear_tipo():
    schema = POcorrenciasUpdateSchema(tipo="")
    assert schema.tipo is None
