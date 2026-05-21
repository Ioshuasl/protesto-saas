from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException

from packages.v1.administrativo.schemas.p_especie_schema import PEspecieSaveSchema
from packages.v1.administrativo.services.p_especie.go.p_especie_save_service import SaveService


@pytest.mark.unit
def test_save_service_raises_409_when_duplicate_especie():
    especie_schema = PEspecieSaveSchema(especie="DMI", descricao="Duplicata")

    with patch(
        "packages.v1.administrativo.services.p_especie.go.p_especie_save_service.GetByEspecieRepository"
    ) as especie_mock:
        especie_mock.return_value.execute.return_value = {"especie_id": 1}

        with pytest.raises(HTTPException) as exc:
            SaveService().execute(especie_schema)

    assert exc.value.status_code == 409


@pytest.mark.unit
def test_save_service_generates_id_and_persists_when_valid():
    especie_schema = PEspecieSaveSchema(especie="ZZZ", descricao="Espécie Teste API")

    with patch(
        "packages.v1.administrativo.services.p_especie.go.p_especie_save_service.GetByEspecieRepository"
    ) as especie_mock, patch(
        "packages.v1.administrativo.services.p_especie.go.p_especie_save_service.GenerateService"
    ) as generate_mock, patch(
        "packages.v1.administrativo.services.p_especie.go.p_especie_save_service.SaveAction"
    ) as save_action_mock:
        especie_mock.return_value.execute.return_value = None
        generate_mock.return_value.execute.return_value = MagicMock(sequencia=9001)
        save_action_mock.return_value.execute.return_value = {
            "especie_id": 9001,
            "especie": "ZZZ",
            "descricao": "Espécie Teste API",
        }

        result = SaveService().execute(especie_schema)

    assert result["especie_id"] == 9001
    assert especie_schema.especie_id == 9001
