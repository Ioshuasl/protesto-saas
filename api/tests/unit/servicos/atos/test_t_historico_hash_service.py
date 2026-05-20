import pytest
from fastapi import HTTPException

from packages.v1.servicos.atos.schemas.t_historico_schema import THistoricoHashSchema
from packages.v1.servicos.atos.services.t_historico.go.t_historico_hash_service import (
    THistoricoHashService,
)


def test_t_historico_hash_deve_gerar_hash_e_retornar_registros(monkeypatch):
    expected = [{"HISTORICO_ID": 1}]

    def fake_hash(value):
        assert value == "tsp800"
        return "hash-gerado"

    def fake_execute(self, data):
        assert data.hash_input == "tsp800"
        assert data.hash == "hash-gerado"
        return expected

    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_historico.go.t_historico_hash_service.Sha256Crypt.execute",
        fake_hash,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.actions.t_historico.t_historico_hash_action.THistoricoHashAction.execute",
        fake_execute,
    )

    response = THistoricoHashService().execute(THistoricoHashSchema(hash_input="tsp800"))

    assert response == expected


def test_t_historico_hash_deve_retornar_404_quando_nao_localizar(monkeypatch):
    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_historico.go.t_historico_hash_service.Sha256Crypt.execute",
        lambda value: "hash-gerado",
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.actions.t_historico.t_historico_hash_action.THistoricoHashAction.execute",
        lambda self, data: [],
    )

    with pytest.raises(HTTPException) as exc:
        THistoricoHashService().execute(THistoricoHashSchema(hash_input="tsp800"))

    assert exc.value.status_code == 404
