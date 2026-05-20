from decimal import Decimal

import pytest
from fastapi import HTTPException

from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoAnteriorUpdateSchema
from packages.v1.servicos.atos.services.t_ato.go.t_ato_anterior_update_service import (
    TAtoAnteriorUpdateService,
)


def test_deve_atualizar_parcialmente_quando_houver_campos(monkeypatch):
    expected = {"ato_id": Decimal("10"), "ato_anterior_origem": "S"}

    def fake_execute(self, data):
        assert data.ato_id == Decimal("10")
        assert data.ato_anterior_origem == "S"
        return expected

    monkeypatch.setattr(
        "packages.v1.servicos.atos.actions.t_ato.t_ato_anterior_update_action.TAtoAnteriorUpdateAction.execute",
        fake_execute,
    )

    data = TAtoAnteriorUpdateSchema(ato_id=Decimal("10"), ato_anterior_origem="S")
    response = TAtoAnteriorUpdateService().execute(data)
    assert response == expected


def test_deve_retornar_400_quando_payload_vazio():
    with pytest.raises(HTTPException) as exc:
        TAtoAnteriorUpdateService().execute(TAtoAnteriorUpdateSchema(ato_id=Decimal("10")))
    assert exc.value.status_code == 400


def test_deve_retornar_404_quando_ato_nao_existir(monkeypatch):
    def fake_execute(self, data):
        return None

    monkeypatch.setattr(
        "packages.v1.servicos.atos.actions.t_ato.t_ato_anterior_update_action.TAtoAnteriorUpdateAction.execute",
        fake_execute,
    )

    with pytest.raises(HTTPException) as exc:
        TAtoAnteriorUpdateService().execute(
            TAtoAnteriorUpdateSchema(ato_id=Decimal("999"), ato_anterior_origem="S")
        )
    assert exc.value.status_code == 404
