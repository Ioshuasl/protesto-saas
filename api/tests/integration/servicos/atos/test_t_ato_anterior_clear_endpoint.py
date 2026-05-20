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
    def clear_ato_anterior(self, data):
        return {
            "message": "Dados do ato anterior limpos com sucesso.",
            "data": {
                "ato_id": int(data.ato_id),
                "ato_anterior_ato_id": None,
            },
        }


def _build_client(fake_current_user):
    app = FastAPI()
    app.include_router(t_ato_endpoint.router, prefix="/servicos/atos/t_ato")
    app.dependency_overrides[t_ato_endpoint.get_current_user] = lambda: fake_current_user
    return TestClient(app)


def test_t_ato_anterior_clear_put_deve_retornar_sucesso(monkeypatch, fake_current_user):
    monkeypatch.setattr(t_ato_endpoint, "controller", _FakeController)
    client = _build_client(fake_current_user)

    response = client.put("/servicos/atos/t_ato/123/ato-anterior/limpar")

    assert response.status_code == 200
    payload = response.json()
    assert payload["message"] == "Dados do ato anterior limpos com sucesso."
    assert payload["data"]["ato_id"] == 123
    assert payload["data"]["ato_anterior_ato_id"] is None


def test_t_ato_anterior_clear_deve_retornar_405_para_metodo_invalido(fake_current_user):
    client = _build_client(fake_current_user)

    response = client.get("/servicos/atos/t_ato/123/ato-anterior/limpar")

    assert response.status_code == 405
