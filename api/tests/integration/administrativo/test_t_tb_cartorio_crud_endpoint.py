from fastapi import FastAPI
from fastapi.testclient import TestClient

from packages.v1.administrativo.endpoints import t_tb_cartorio_endpoint


class _FakeController:
    def index(self):
        return {"message": "ok", "data": []}

    def show(self, data):
        return {"message": "ok", "data": {"tb_cartorio_id": data.tb_cartorio_id}}

    def save(self, data):
        return {"message": "ok", "data": {"tb_cartorio_id": data.tb_cartorio_id or 1}}

    def delete(self, data):
        return {"message": "ok", "data": {"tb_cartorio_id": data.tb_cartorio_id}}


def _build_client(fake_current_user):
    app = FastAPI()
    app.include_router(t_tb_cartorio_endpoint.router, prefix="/administrativo/t_tb_cartorio")
    app.dependency_overrides[t_tb_cartorio_endpoint.get_current_user] = lambda: fake_current_user
    return TestClient(app)


def test_t_tb_cartorio_show_deve_retornar_sucesso(monkeypatch, fake_current_user):
    monkeypatch.setattr(t_tb_cartorio_endpoint, "controller", _FakeController())
    client = _build_client(fake_current_user)

    response = client.get("/administrativo/t_tb_cartorio/1")

    assert response.status_code == 200


def test_t_tb_cartorio_save_deve_retornar_sucesso(monkeypatch, fake_current_user):
    monkeypatch.setattr(t_tb_cartorio_endpoint, "controller", _FakeController())
    client = _build_client(fake_current_user)

    payload = {
        "tb_cartorio_id": 1,
        "descricao": "Cartorio A",
        "municipio_id": 1,
        "descricao_municipio": "Cidade A",
        "cns": "1234567890",
    }

    response = client.post("/administrativo/t_tb_cartorio/", json=payload)

    assert response.status_code == 201


def test_t_tb_cartorio_delete_deve_retornar_sucesso(monkeypatch, fake_current_user):
    monkeypatch.setattr(t_tb_cartorio_endpoint, "controller", _FakeController())
    client = _build_client(fake_current_user)

    response = client.delete("/administrativo/t_tb_cartorio/1")

    assert response.status_code == 200
