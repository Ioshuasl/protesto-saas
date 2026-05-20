from decimal import Decimal

import pytest
from fastapi import HTTPException

from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoAnteriorClearSchema
from packages.v1.servicos.atos.services.t_ato.go.t_ato_anterior_clear_service import (
    TAtoAnteriorClearService,
)


def test_deve_limpar_dados_ato_anterior_quando_ato_existir(monkeypatch):
    expected = {"ato_id": Decimal("10"), "ato_anterior_ato_id": None}

    def fake_execute(self, data):
        assert data.ato_id == Decimal("10")
        return expected

    monkeypatch.setattr(
        "packages.v1.servicos.atos.actions.t_ato.t_ato_anterior_clear_action.TAtoAnteriorClearAction.execute",
        fake_execute,
    )

    response = TAtoAnteriorClearService().execute(
        TAtoAnteriorClearSchema(ato_id=Decimal("10"), usuario_id=Decimal("1"))
    )
    assert response == expected


def test_deve_retornar_404_quando_ato_nao_existir(monkeypatch):
    def fake_execute(self, data):
        return None

    monkeypatch.setattr(
        "packages.v1.servicos.atos.actions.t_ato.t_ato_anterior_clear_action.TAtoAnteriorClearAction.execute",
        fake_execute,
    )

    with pytest.raises(HTTPException) as exc:
        TAtoAnteriorClearService().execute(
            TAtoAnteriorClearSchema(ato_id=Decimal("999"), usuario_id=Decimal("1"))
        )
    assert exc.value.status_code == 404
