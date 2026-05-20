from decimal import Decimal
from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoIdSchema
from packages.v1.servicos.atos.services.t_ato.go.t_ato_retirar_lavratura_service import (
    TAtoRetirarLavraturaService,
)


def test_deve_retirar_lavratura_e_liberar_selo(monkeypatch):
    show_calls = {"count": 0}

    def fake_ato_show(self, data):
        show_calls["count"] += 1

        if show_calls["count"] == 1:
            return SimpleNamespace(
                ato_id=data.ato_id,
                ato_tipo_id=39,
                ato_anterior_ato_id=None,
                situacao_ato="3",
                livro_andamento_id=7,
                folha_inicial=Decimal(11),
                folha_final=Decimal(12),
                folha_atual=Decimal(12),
                protocolo=Decimal(123),
                selo_livro_id=55,
            )

        return SimpleNamespace(
            ato_id=data.ato_id,
            ato_tipo_id=39,
            situacao_ato=2,
            livro_andamento_id=None,
            selo_livro_id=None,
        )

    def fake_ato_tipo_show(self, data):
        return SimpleNamespace(ato_tipo_id=data.ato_tipo_id, possui_ato_anterior="N")

    def fake_is_last_lavrado(self, **kwargs):
        assert kwargs["ato_id"] == 10
        assert kwargs["livro_andamento_id"] == 7
        assert kwargs["protocolo"] == Decimal(123)
        assert kwargs["folha_final"] == Decimal(12)
        return True

    def fake_caixa_item_show(self, data):
        assert data.tabela == "T_ATO"
        assert data.campo_id == 10
        return SimpleNamespace(caixa_item_id=511717)

    def fake_retirar_lavratura(self, data):
        assert data.ato_id == 10
        return {"ato_id": data.ato_id}

    def fake_livro_andamento_update(self, data):
        assert data.livro_andamento_id == 7
        assert data.folha_atual == Decimal(10)
        return SimpleNamespace(livro_andamento_id=data.livro_andamento_id)

    def fake_selo_update(self, data):
        assert data.selo_livro_id == 55
        assert data.selo_situacao_id == 1
        assert data.descricao is None
        assert data.tabela is None
        assert data.campo_id is None
        assert data.valor_total is None
        return SimpleNamespace(selo_livro_id=data.selo_livro_id)

    def fake_caixa_item_delete(self, data):
        assert data.tabela == "T_ATO"
        assert data.campo_id == 10
        return SimpleNamespace(caixa_item_id=511717)

    def fake_sequencia_delete(self, data):
        assert data.sequencia == 511717
        assert data.tabela == "C_CAIXA_ITEM"
        return SimpleNamespace(sequencia=data.sequencia)

    def fake_historico_save(self, data):
        assert data.campo == "Retirada de lavratura"
        assert data.usuario_id == 1
        return SimpleNamespace(historico_id=1)

    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_retirar_lavratura_service.TAtoShowService.execute",
        fake_ato_show,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_retirar_lavratura_service.TAtoTipoShowAction.execute",
        fake_ato_tipo_show,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_retirar_lavratura_service.TAtoIsLastLavradoByProtocoloFolhaRepository.execute",
        fake_is_last_lavrado,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_retirar_lavratura_service.CaixaItemShowByTabelaCampoRepository.execute",
        fake_caixa_item_show,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_retirar_lavratura_service.TAtoRetirarLavraturaRepository.execute",
        fake_retirar_lavratura,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_retirar_lavratura_service.TLivroAndamentoUpdateAction.execute",
        fake_livro_andamento_update,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_retirar_lavratura_service.GSeloLivroUpdateService.execute",
        fake_selo_update,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_retirar_lavratura_service.CaixaItemDeleteByTabelaCampoRepository.execute",
        fake_caixa_item_delete,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_retirar_lavratura_service.SequenciaDeleteService.execute",
        fake_sequencia_delete,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_retirar_lavratura_service.THistoricoSaveService.execute",
        fake_historico_save,
    )

    data = TAtoIdSchema(ato_id=10, usuario_id=1)
    response = TAtoRetirarLavraturaService().execute(data)

    assert response.ato_id == 10
    assert response.situacao_ato == 2


def test_deve_retornar_422_quando_ato_lavrado_nao_tem_selo(monkeypatch):
    def fake_ato_show(self, data):
        return SimpleNamespace(
            ato_id=data.ato_id,
            ato_tipo_id=39,
            ato_anterior_ato_id=None,
            situacao_ato="3",
            livro_andamento_id=7,
            folha_inicial=Decimal(11),
            folha_final=Decimal(12),
            folha_atual=Decimal(12),
            protocolo=Decimal(123),
            selo_livro_id=None,
        )

    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_retirar_lavratura_service.TAtoShowService.execute",
        fake_ato_show,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_retirar_lavratura_service.TAtoTipoShowAction.execute",
        lambda self, data: SimpleNamespace(ato_tipo_id=data.ato_tipo_id, possui_ato_anterior="N"),
    )

    data = TAtoIdSchema(ato_id=10, usuario_id=1)

    with pytest.raises(HTTPException) as exc:
        TAtoRetirarLavraturaService().execute(data)

    assert exc.value.status_code == 422
    assert exc.value.detail == "[TR427] Ato sem selo vinculado para retirada da lavratura."
