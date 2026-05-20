from packages.v1.servicos.atos.repositories.t_historico.t_historico_hash_repository import (
    THistoricoHashRepository,
)
from packages.v1.servicos.atos.schemas.t_historico_schema import THistoricoHashSchema


def test_t_historico_hash_repository_deve_consultar_por_hash(monkeypatch):
    captured = {}

    def fake_fetch_all(self, sql, params):
        captured["sql"] = sql
        captured["params"] = params
        return [{"HISTORICO_ID": 1}]

    monkeypatch.setattr(
        "abstracts.repository.BaseRepository.fetch_all",
        fake_fetch_all,
    )

    response = THistoricoHashRepository().execute(
        THistoricoHashSchema(hash_input="tsp800", hash="hash-gerado")
    )

    assert response == [{"HISTORICO_ID": 1}]
    assert "FROM T_HISTORICO TH" in captured["sql"]
    assert "WHERE TH.HASH = :hash" in captured["sql"]
    assert "ORDER BY TH.DATA DESC" in captured["sql"]
    assert captured["params"] == {"hash": "hash-gerado"}
