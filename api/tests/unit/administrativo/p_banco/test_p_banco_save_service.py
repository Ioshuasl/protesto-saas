from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException

from packages.v1.administrativo.schemas.p_banco_schema import PBancoSaveSchema
from packages.v1.administrativo.services.p_banco.go.p_banco_save_service import SaveService


@pytest.mark.unit
def test_save_service_raises_409_when_duplicate_codigo():
    banco_schema = PBancoSaveSchema(
        codigo_banco="001",
        descricao="Banco Teste",
        layout_id=25,
        apontamento_pag_posterior="S",
        custas_na_confirmacao="N",
    )

    with patch(
        "packages.v1.administrativo.services.p_banco.go.p_banco_save_service.GetByCodigoRepository"
    ) as codigo_mock, patch(
        "packages.v1.administrativo.services.p_banco.go.p_banco_save_service.LayoutExistsRepository"
    ) as layout_mock:
        codigo_mock.return_value.execute.return_value = {"banco_id": 1}
        layout_mock.return_value.execute.return_value = True

        with pytest.raises(HTTPException) as exc:
            SaveService().execute(banco_schema)

    assert exc.value.status_code == 409


@pytest.mark.unit
def test_save_service_raises_404_when_layout_missing():
    banco_schema = PBancoSaveSchema(
        codigo_banco="001",
        descricao="Banco Teste",
        layout_id=25,
        apontamento_pag_posterior="S",
        custas_na_confirmacao="N",
    )

    with patch(
        "packages.v1.administrativo.services.p_banco.go.p_banco_save_service.GetByCodigoRepository"
    ) as codigo_mock, patch(
        "packages.v1.administrativo.services.p_banco.go.p_banco_save_service.LayoutExistsRepository"
    ) as layout_mock:
        codigo_mock.return_value.execute.return_value = None
        layout_mock.return_value.execute.return_value = False

        with pytest.raises(HTTPException) as exc:
            SaveService().execute(banco_schema)

    assert exc.value.status_code == 404


@pytest.mark.unit
def test_save_service_generates_id_and_persists_when_valid():
    banco_schema = PBancoSaveSchema(
        codigo_banco="ZZZ-API-TEST",
        descricao="Banco API Teste",
        layout_id=25,
        apontamento_pag_posterior="S",
        custas_na_confirmacao="N",
    )

    with patch(
        "packages.v1.administrativo.services.p_banco.go.p_banco_save_service.GetByCodigoRepository"
    ) as codigo_mock, patch(
        "packages.v1.administrativo.services.p_banco.go.p_banco_save_service.LayoutExistsRepository"
    ) as layout_mock, patch(
        "packages.v1.administrativo.services.p_banco.go.p_banco_save_service.GenerateService"
    ) as generate_mock, patch(
        "packages.v1.administrativo.services.p_banco.go.p_banco_save_service.SaveAction"
    ) as save_action_mock:
        codigo_mock.return_value.execute.return_value = None
        layout_mock.return_value.execute.return_value = True
        generate_mock.return_value.execute.return_value = MagicMock(sequencia=999001)
        save_action_mock.return_value.execute.return_value = {"banco_id": 999001}

        result = SaveService().execute(banco_schema)

    assert result["banco_id"] == 999001
    assert banco_schema.banco_id == 999001
