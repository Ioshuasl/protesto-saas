from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException

from packages.v1.administrativo.schemas.g_feriado_schema import GFeriadoSaveSchema
from packages.v1.administrativo.services.g_feriado.go.g_feriado_save_service import (
    SaveService,
)


@pytest.mark.unit
def test_save_service_raises_409_when_duplicate_data_tipo():
    feriado_schema = GFeriadoSaveSchema(
        data=datetime(2026, 1, 1),
        descricao="Confraternização Universal",
        tipo="F",
        situacao="A",
    )

    with patch(
        "packages.v1.administrativo.services.g_feriado.go.g_feriado_save_service.GetByDataTipoRepository"
    ) as repository_mock:
        repository_mock.return_value.execute.return_value = {"feriado_id": 99}

        with pytest.raises(HTTPException) as exc:
            SaveService().execute(feriado_schema)

    assert exc.value.status_code == 409


@pytest.mark.unit
def test_save_service_generates_id_and_persists_when_unique():
    feriado_schema = GFeriadoSaveSchema(
        data=datetime(2026, 12, 25),
        descricao="Natal",
        tipo="F",
        situacao="A",
    )

    with patch(
        "packages.v1.administrativo.services.g_feriado.go.g_feriado_save_service.GetByDataTipoRepository"
    ) as repository_mock, patch(
        "packages.v1.administrativo.services.g_feriado.go.g_feriado_save_service.GenerateService"
    ) as generate_mock, patch(
        "packages.v1.administrativo.services.g_feriado.go.g_feriado_save_service.SaveAction"
    ) as save_action_mock:
        repository_mock.return_value.execute.return_value = None
        generate_mock.return_value.execute.return_value = MagicMock(sequencia=10)
        save_action_mock.return_value.execute.return_value = {"feriado_id": 10}

        result = SaveService().execute(feriado_schema)

    assert result["feriado_id"] == 10
    assert feriado_schema.feriado_id == 10
