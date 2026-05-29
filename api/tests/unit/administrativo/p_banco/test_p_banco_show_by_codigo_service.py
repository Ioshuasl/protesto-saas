from unittest.mock import patch

import pytest
from fastapi import HTTPException

from packages.v1.administrativo.schemas.p_banco_schema import PBancoCodigoSchema
from packages.v1.administrativo.services.p_banco.go.p_banco_show_by_codigo_service import (
    ShowByCodigoService,
)


@pytest.mark.unit
def test_show_by_codigo_service_raises_404_when_not_found():
    codigo_schema = PBancoCodigoSchema(codigo_banco="033")

    with patch(
        "packages.v1.administrativo.services.p_banco.go.p_banco_show_by_codigo_service.ShowByCodigoAction"
    ) as action_mock:
        action_mock.return_value.execute.return_value = None

        with pytest.raises(HTTPException) as exc:
            ShowByCodigoService().execute(codigo_schema)

    assert exc.value.status_code == 404


@pytest.mark.unit
def test_show_by_codigo_service_returns_banco_when_found():
    codigo_schema = PBancoCodigoSchema(codigo_banco="033")
    expected = {"banco_id": 1, "codigo_banco": "033", "descricao": "Santander"}

    with patch(
        "packages.v1.administrativo.services.p_banco.go.p_banco_show_by_codigo_service.ShowByCodigoAction"
    ) as action_mock:
        action_mock.return_value.execute.return_value = expected

        result = ShowByCodigoService().execute(codigo_schema)

    assert result == expected
