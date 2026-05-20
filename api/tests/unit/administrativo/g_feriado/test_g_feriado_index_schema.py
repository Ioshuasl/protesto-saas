import pytest
from pydantic import ValidationError

from packages.v1.administrativo.schemas.g_feriado_schema import GFeriadoIndexSchema


@pytest.mark.unit
def test_index_schema_rejects_invalid_ano_filter():
    with pytest.raises(ValidationError):
        GFeriadoIndexSchema(ano="abc")


@pytest.mark.unit
def test_index_schema_rejects_unknown_filter():
    with pytest.raises(ValidationError):
        GFeriadoIndexSchema(ano=2026, filtro_generico="x")
