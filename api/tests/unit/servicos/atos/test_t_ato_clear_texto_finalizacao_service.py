import pytest
from fastapi import HTTPException

from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoClearTextoFinalizacaoSchema
from packages.v1.servicos.atos.services.t_ato.go.t_ato_clear_texto_finalizacao_service import (
    TAtoClearTextoFinalizacaoService,
)


def test_deve_limpar_finalizacao_livro_quando_tipo_1(monkeypatch):
    def fake_show_execute(self, data):
        return {"ato_id": data.ato_id}

    def fake_action_execute(self, data):
        assert data.coluna == "texto_finalizacao"
        return {"ato_id": data.ato_id, "texto_finalizacao": None}

    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_show_service.TAtoShowService.execute",
        fake_show_execute,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.actions.t_ato.t_ato_clear_texto_finalizacao_action.TAtoClearTextoFinalizacaoAction.execute",
        fake_action_execute,
    )

    data = TAtoClearTextoFinalizacaoSchema(ato_id=10, tipo_finalizacao=1, usuario_id=1)
    response = TAtoClearTextoFinalizacaoService().execute(data)

    assert response["texto_finalizacao"] is None


def test_deve_limpar_finalizacao_traslado_quando_tipo_2(monkeypatch):
    def fake_show_execute(self, data):
        return {"ato_id": data.ato_id}

    def fake_action_execute(self, data):
        assert data.coluna == "texto_finalizacao_traslado"
        return {"ato_id": data.ato_id, "texto_finalizacao": None}

    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_show_service.TAtoShowService.execute",
        fake_show_execute,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.actions.t_ato.t_ato_clear_texto_finalizacao_action.TAtoClearTextoFinalizacaoAction.execute",
        fake_action_execute,
    )

    data = TAtoClearTextoFinalizacaoSchema(ato_id=11, tipo_finalizacao=2, usuario_id=1)
    response = TAtoClearTextoFinalizacaoService().execute(data)

    assert response["texto_finalizacao"] is None


def test_deve_retornar_404_quando_ato_nao_existir(monkeypatch):
    def fake_show_execute(self, data):
        return None

    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_show_service.TAtoShowService.execute",
        fake_show_execute,
    )

    data = TAtoClearTextoFinalizacaoSchema(ato_id=999999, tipo_finalizacao=1, usuario_id=1)

    with pytest.raises(HTTPException) as exc:
        TAtoClearTextoFinalizacaoService().execute(data)

    assert exc.value.status_code == 404
