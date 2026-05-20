from unittest.mock import patch

import pytest
from fastapi import HTTPException

from packages.v1.administrativo.schemas.p_banco_schema import PBancoIdSchema
from packages.v1.administrativo.services.p_banco.go.p_banco_delete_service import DeleteService


@pytest.mark.unit
def test_delete_service_raises_409_when_titulos_linked():
    banco_schema = PBancoIdSchema(banco_id=300028)

    with patch(
        "packages.v1.administrativo.services.p_banco.go.p_banco_delete_service.ShowAction"
    ) as show_mock, patch(
        "packages.v1.administrativo.services.p_banco.go.p_banco_delete_service.CountTituloRepository"
    ) as count_mock:
        show_mock.return_value.execute.return_value = {"banco_id": 300028}
        count_mock.return_value.execute.return_value = 2

        with pytest.raises(HTTPException) as exc:
            DeleteService().execute(banco_schema)

    assert exc.value.status_code == 409
