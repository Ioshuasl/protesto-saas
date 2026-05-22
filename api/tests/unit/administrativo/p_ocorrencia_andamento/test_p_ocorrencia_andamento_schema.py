import pytest

from packages.v1.administrativo.schemas.p_ocorrencia_andamento_schema import (
    POcorrenciaAndamentoSaveSchema,
    normalize_codigo,
)


@pytest.mark.unit
def test_normalize_codigo_uppercases():
    assert normalize_codigo("  ab  ") == "AB"


@pytest.mark.unit
def test_normalize_codigo_rejects_empty():
    with pytest.raises(ValueError, match="obrigatório"):
        normalize_codigo("  ")


@pytest.mark.unit
def test_save_schema_normalizes_codigo():
    schema = POcorrenciaAndamentoSaveSchema(codigo="zz", descricao="Teste")
    assert schema.codigo == "ZZ"
    assert schema.descricao == "Teste"
