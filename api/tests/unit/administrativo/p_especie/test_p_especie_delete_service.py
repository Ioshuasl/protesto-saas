from unittest.mock import patch

import pytest
from fastapi import HTTPException

from packages.v1.administrativo.schemas.p_especie_schema import PEspecieIdSchema
from packages.v1.administrativo.services.p_especie.go.p_especie_delete_service import DeleteService


@pytest.mark.unit
def test_delete_service_raises_409_when_titulos_linked():
    especie_schema = PEspecieIdSchema(especie_id=1)

    with patch(
        "packages.v1.administrativo.services.p_especie.go.p_especie_delete_service.ShowAction"
    ) as show_mock, patch(
        "packages.v1.administrativo.services.p_especie.go.p_especie_delete_service.CountByEspecieRepository"
    ) as count_mock:
        show_mock.return_value.execute.return_value = {"especie_id": 1}
        count_mock.return_value.execute.return_value = 2

        with pytest.raises(HTTPException) as exc:
            DeleteService().execute(especie_schema)

    assert exc.value.status_code == 409
