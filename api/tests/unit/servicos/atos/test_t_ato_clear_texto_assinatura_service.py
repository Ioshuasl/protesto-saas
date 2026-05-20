import pytest
from fastapi import HTTPException

from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoClearTextoAssinaturaSchema
from packages.v1.servicos.atos.services.t_ato.go.t_ato_clear_texto_assinatura_service import (
    TAtoClearTextoAssinaturaService,
)


def test_deve_limpar_assinatura_normal_quando_tipo_1(monkeypatch):
    def fake_show_execute(self, data):
        return {"ato_id": data.ato_id}

    def fake_action_execute(self, data):
        assert data.coluna == "texto_assinatura"
        return {"ato_id": data.ato_id, "texto_assinatura": None}

    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_show_service.TAtoShowService.execute",
        fake_show_execute,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.actions.t_ato.t_ato_clear_texto_assinatura_action.TAtoClearTextoAssinaturaAction.execute",
        fake_action_execute,
    )

    data = TAtoClearTextoAssinaturaSchema(ato_id=10, tipo_assinatura=1, usuario_id=1)
    response = TAtoClearTextoAssinaturaService().execute(data)

    assert response["texto_assinatura"] is None


def test_deve_limpar_assinatura_traslado_quando_tipo_2(monkeypatch):
    def fake_show_execute(self, data):
        return {"ato_id": data.ato_id}

    def fake_action_execute(self, data):
        assert data.coluna == "texto_assinatura_traslado"
        return {"ato_id": data.ato_id, "texto_assinatura": None}

    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_show_service.TAtoShowService.execute",
        fake_show_execute,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.actions.t_ato.t_ato_clear_texto_assinatura_action.TAtoClearTextoAssinaturaAction.execute",
        fake_action_execute,
    )

    data = TAtoClearTextoAssinaturaSchema(ato_id=11, tipo_assinatura=2, usuario_id=1)
    response = TAtoClearTextoAssinaturaService().execute(data)

    assert response["texto_assinatura"] is None


def test_deve_retornar_404_quando_ato_nao_existir(monkeypatch):
    def fake_show_execute(self, data):
        return None

    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_show_service.TAtoShowService.execute",
        fake_show_execute,
    )

    data = TAtoClearTextoAssinaturaSchema(ato_id=999999, tipo_assinatura=1, usuario_id=1)

    with pytest.raises(HTTPException) as exc:
        TAtoClearTextoAssinaturaService().execute(data)

    assert exc.value.status_code == 404
