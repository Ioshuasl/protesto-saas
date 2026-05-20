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
    def ato_anterior(self, data):
        return {
            "message": "Dados do ato anterior localizados com sucesso.",
            "data": {
                "ato_anterior_origem": "S",
                "ato_anterior_livro": 12,
                "ato_anterior_finicial": "10",
                "ato_anterior_tb_cartorio_id": 2,
                "ato_anterior_outorgante": "OUTORGANTE",
                "ato_anterior_observacao": "OBS",
                "ato_anterior_ato_id": 99,
                "ato_anterior_data": "2025-01-01T00:00:00",
                "ato_anterior_anotacao_adicional": "YWJj",
                "ato_anterior_ato_tipo_id": 8,
                "ato_anterior_valor_documento": 123.45,
            },
        }


def _build_client(fake_current_user):
    app = FastAPI()
    app.include_router(t_ato_endpoint.router, prefix="/servicos/atos/t_ato")
    app.dependency_overrides[t_ato_endpoint.get_current_user] = lambda: fake_current_user
    return TestClient(app)


def test_t_ato_ato_anterior_get_deve_retornar_sucesso(monkeypatch, fake_current_user):
    monkeypatch.setattr(t_ato_endpoint, "controller", _FakeController)
    client = _build_client(fake_current_user)

    response = client.get("/servicos/atos/t_ato/ato-anterior?ato_id=123")

    assert response.status_code == 200
    payload = response.json()
    assert payload["message"] == "Dados do ato anterior localizados com sucesso."
    assert payload["data"]["ato_anterior_ato_id"] == 99


def test_t_ato_ato_anterior_deve_retornar_405_para_metodo_invalido(fake_current_user):
    client = _build_client(fake_current_user)

    response = client.post("/servicos/atos/t_ato/ato-anterior?ato_id=123")

    assert response.status_code == 405
