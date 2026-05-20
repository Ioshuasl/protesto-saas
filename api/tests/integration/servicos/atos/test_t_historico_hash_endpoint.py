from fastapi import FastAPI
from fastapi.testclient import TestClient

from packages.v1.servicos.atos.endpoint import t_historico_endpoint


class _FakeController:
    def show_by_hash(self, data):
        return {
            "message": "ok",
            "data": [{"hash_input": data.hash_input}],
        }


def _build_client(fake_current_user):
    app = FastAPI()
    app.include_router(t_historico_endpoint.router, prefix="/servicos/t_historico")
    app.dependency_overrides[t_historico_endpoint.get_current_user] = (
        lambda: fake_current_user
    )
    return TestClient(app)


def test_t_historico_hash_endpoint_deve_retornar_sucesso(
    monkeypatch,
    fake_current_user,
):
    monkeypatch.setattr(t_historico_endpoint, "controller", _FakeController())
    client = _build_client(fake_current_user)

    response = client.get("/servicos/t_historico/hash/tsp800")

    assert response.status_code == 200
    assert response.json()["message"] == "ok"
    assert response.json()["data"][0]["hash_input"] == "tsp800"
