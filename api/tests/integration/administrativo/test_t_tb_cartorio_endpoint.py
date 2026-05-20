from fastapi import FastAPI
from fastapi.testclient import TestClient

from packages.v1.administrativo.endpoints import t_tb_cartorio_endpoint


class _FakeController:
    def index(self):
        return {"message": "ok", "data": []}


def _build_client(fake_current_user):
    app = FastAPI()
    app.include_router(t_tb_cartorio_endpoint.router, prefix="/administrativo/t_tb_cartorio")
    app.dependency_overrides[t_tb_cartorio_endpoint.get_current_user] = lambda: fake_current_user
    return TestClient(app)


def test_t_tb_cartorio_index_deve_retornar_sucesso(monkeypatch, fake_current_user):
    monkeypatch.setattr(t_tb_cartorio_endpoint, "controller", _FakeController())
    client = _build_client(fake_current_user)

    response = client.get("/administrativo/t_tb_cartorio/")

    assert response.status_code == 200
    assert response.json()["message"] == "ok"


def test_t_tb_cartorio_index_deve_retornar_405_para_metodo_invalido(fake_current_user):
    client = _build_client(fake_current_user)

    response = client.put("/administrativo/t_tb_cartorio/")

    assert response.status_code == 405
