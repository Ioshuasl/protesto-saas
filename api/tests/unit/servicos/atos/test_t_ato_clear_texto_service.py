import pytest
from fastapi import HTTPException

from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoClearTextoSchema
from packages.v1.servicos.atos.services.t_ato.go.t_ato_clear_texto_service import (
    TAtoClearTextoService,
)


def test_deve_limpar_texto_quando_ato_existir(monkeypatch):
    expected = {"ato_id": 10, "texto": None}

    def fake_execute(self, data):
        assert data.ato_id == 10
        return expected

    monkeypatch.setattr(
        "packages.v1.servicos.atos.actions.t_ato.t_ato_clear_texto_action.TAtoClearTextoAction.execute",
        fake_execute,
    )

    data = TAtoClearTextoSchema(ato_id=10, usuario_id=1)
    response = TAtoClearTextoService().execute(data)

    assert response == expected


def test_deve_retornar_404_quando_ato_nao_existir(monkeypatch):
    def fake_execute(self, data):
        return None

    monkeypatch.setattr(
        "packages.v1.servicos.atos.actions.t_ato.t_ato_clear_texto_action.TAtoClearTextoAction.execute",
        fake_execute,
    )

    data = TAtoClearTextoSchema(ato_id=999999, usuario_id=1)

    with pytest.raises(HTTPException) as exc:
        TAtoClearTextoService().execute(data)

    assert exc.value.status_code == 404
