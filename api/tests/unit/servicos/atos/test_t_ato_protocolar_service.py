from decimal import Decimal
from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoIdSchema
from packages.v1.servicos.atos.services.t_ato.go.t_ato_protocolar_service import (
    TAtoProtocolarService,
)


def test_deve_protocolar_ato_com_sucesso(monkeypatch):
    def fake_ato_lock_show(self, data):
        assert data.ato_id == 10
        return {"ato_id": Decimal(10), "protocolo": None}

    def fake_generate(self, data):
        assert data.tabela == "ATO_PROTOCOLO"
        assert data.contador is True
        return SimpleNamespace(sequencia=Decimal(8))

    def fake_ato_update(self, data):
        assert data.ato_id == Decimal(10)
        assert data.protocolo == Decimal(8)
        return {
            "ato_id": Decimal(10),
            "protocolo": Decimal(8),
            "data_protocolo": "2026-04-28 10:00:00",
        }

    def fake_historico_save(self, data):
        assert data.tabela == "T_ATO"
        assert data.usuario_id == Decimal(99)
        return SimpleNamespace(historico_id=1)

    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_protocolar_service.TAtoProtocolarLockShowRepository.execute",
        fake_ato_lock_show,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_protocolar_service.GenerateService.execute",
        fake_generate,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_protocolar_service.TAtoProtocolarUpdateRepository.execute",
        fake_ato_update,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_protocolar_service.THistoricoSaveService.execute",
        fake_historico_save,
    )

    response = TAtoProtocolarService().execute(
        TAtoIdSchema(ato_id=Decimal(10), usuario_id=Decimal(99))
    )

    assert response.ato_id == 10.0
    assert response.protocolo == 8.0


def test_deve_retornar_409_quando_ato_ja_protocolado(monkeypatch):
    def fake_ato_lock_show(self, data):
        assert data.ato_id == 10
        return {"ato_id": Decimal(10), "protocolo": Decimal(123)}

    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_protocolar_service.TAtoProtocolarLockShowRepository.execute",
        fake_ato_lock_show,
    )

    with pytest.raises(HTTPException) as exc:
        TAtoProtocolarService().execute(
            TAtoIdSchema(ato_id=Decimal(10), usuario_id=Decimal(99))
        )

    assert exc.value.status_code == 409
    assert exc.value.detail == "[TA409] Este ato ja esta protocolado."


def test_deve_retornar_409_quando_update_concorrente_nao_retorna_linha(monkeypatch):
    def fake_ato_lock_show(self, data):
        return {"ato_id": Decimal(10), "protocolo": None}

    def fake_generate(self, data):
        assert data.tabela == "ATO_PROTOCOLO"
        assert data.contador is True
        return SimpleNamespace(sequencia=Decimal(8))

    def fake_ato_update(self, data):
        return None

    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_protocolar_service.TAtoProtocolarLockShowRepository.execute",
        fake_ato_lock_show,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_protocolar_service.GenerateService.execute",
        fake_generate,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_protocolar_service.TAtoProtocolarUpdateRepository.execute",
        fake_ato_update,
    )

    with pytest.raises(HTTPException) as exc:
        TAtoProtocolarService().execute(
            TAtoIdSchema(ato_id=Decimal(10), usuario_id=Decimal(99))
        )

    assert exc.value.status_code == 409
    assert exc.value.detail == "[TA409] Este ato ja esta protocolado."
