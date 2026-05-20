import pytest

from packages.v1.administrativo.schemas.g_feriado_schema import (
    GFeriadoIndexSchema,
    normalize_situacao,
    normalize_tipo,
)


@pytest.mark.unit
@pytest.mark.parametrize("raw,expected", [("F", "F"), ("f", "F"), ("V", "V")])
def test_normalize_tipo(raw, expected):
    assert normalize_tipo(raw) == expected


@pytest.mark.unit
def test_normalize_tipo_rejects_label():
    with pytest.raises(ValueError, match="F \\(fixo\\)"):
        normalize_tipo("Fixo")


@pytest.mark.unit
@pytest.mark.parametrize("raw,expected", [("A", "A"), ("a", "A"), ("I", "I")])
def test_normalize_situacao(raw, expected):
    assert normalize_situacao(raw) == expected


@pytest.mark.unit
def test_normalize_situacao_rejects_label():
    with pytest.raises(ValueError, match="A \\(ativo\\)"):
        normalize_situacao("Ativo")


@pytest.mark.unit
def test_index_schema_accepts_siglas():
    schema = GFeriadoIndexSchema(ano=2026, tipo="F", situacao="A")
    assert schema.tipo == "F"
    assert schema.situacao == "A"
