from datetime import datetime
from decimal import Decimal

import pytest
from fastapi import HTTPException

from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoIdSchema
from packages.v1.servicos.atos.services.t_ato.go.t_ato_ato_anterior_service import (
    TAtoAtoAnteriorService,
)


def test_deve_retornar_dados_ato_anterior_quando_existir(monkeypatch):
    expected = {
        "ato_anterior_origem": "S",
        "ato_anterior_livro": Decimal("12"),
        "ato_anterior_finicial": "10",
        "ato_anterior_tb_cartorio_id": Decimal("2"),
        "ato_anterior_outorgante": "OUTORGANTE",
        "ato_anterior_observacao": "OBS",
        "ato_anterior_ato_id": Decimal("99"),
        "ato_anterior_data": datetime(2025, 1, 1),
        "ato_anterior_anotacao_adicional": b"abc",
        "ato_anterior_ato_tipo_id": Decimal("8"),
        "ato_anterior_valor_documento": Decimal("123.45"),
    }

    def fake_execute(self, data):
        assert data.ato_id == Decimal("100")
        return expected

    monkeypatch.setattr(
        "packages.v1.servicos.atos.actions.t_ato.t_ato_ato_anterior_action.TAtoAtoAnteriorAction.execute",
        fake_execute,
    )

    response = TAtoAtoAnteriorService().execute(TAtoIdSchema(ato_id=Decimal("100")))
    assert response == expected


def test_deve_retornar_404_quando_nao_existir_ato_anterior(monkeypatch):
    def fake_execute(self, data):
        return None

    monkeypatch.setattr(
        "packages.v1.servicos.atos.actions.t_ato.t_ato_ato_anterior_action.TAtoAtoAnteriorAction.execute",
        fake_execute,
    )

    with pytest.raises(HTTPException) as exc:
        TAtoAtoAnteriorService().execute(TAtoIdSchema(ato_id=Decimal("1")))

    assert exc.value.status_code == 404
