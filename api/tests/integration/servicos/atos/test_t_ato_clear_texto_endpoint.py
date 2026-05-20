from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest

try:
    from packages.v1.servicos.atos.endpoint import t_ato_endpoint
except ModuleNotFoundError as exc:
    pytest.skip(
        f"Dependencia ausente para importar endpoint real: {exc}",
        allow_module_level=True,
    )


class _FakeController:
    def clear_texto(self, data):
        return {
            "message": "Texto de T_ATO limpo com sucesso.",
            "data": {"ato_id": int(data.ato_id), "texto": None},
        }


def _build_client(fake_current_user):
    app = FastAPI()
    app.include_router(t_ato_endpoint.router, prefix="/servicos/atos/t_ato")
    app.dependency_overrides[t_ato_endpoint.get_current_user] = lambda: fake_current_user
    return TestClient(app)


def test_t_ato_clear_texto_put_deve_retornar_sucesso(monkeypatch, fake_current_user):
    monkeypatch.setattr(t_ato_endpoint, "controller", _FakeController)
    client = _build_client(fake_current_user)

    response = client.put("/servicos/atos/t_ato/123/texto/limpar")

    assert response.status_code == 200
    payload = response.json()
    assert payload["message"] == "Texto de T_ATO limpo com sucesso."
    assert payload["data"]["ato_id"] == 123
    assert payload["data"]["texto"] is None


def test_t_ato_clear_texto_deve_retornar_405_para_metodo_invalido(fake_current_user):
    client = _build_client(fake_current_user)

    response = client.get("/servicos/atos/t_ato/123/texto/limpar")

    assert response.status_code == 405
