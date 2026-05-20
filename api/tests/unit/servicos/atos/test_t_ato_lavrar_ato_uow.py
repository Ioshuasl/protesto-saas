from decimal import Decimal
from types import SimpleNamespace

from packages.v1.administrativo.schemas.c_caixa_item_schema import CaixaItemSchema
from packages.v1.administrativo.schemas.g_selo_livro_schema import GSeloLivroUpdateSchema
from packages.v1.administrativo.schemas.t_livro_andamento_schema import (
    TLivroAndamentoUpdateSchema,
)
from packages.v1.servicos.atos.repositories.t_ato.t_ato_lavrar_ato_repository import (
    TAtoLavrarAtoRepository,
)
from packages.v1.servicos.atos.uow.t_ato.t_ato_lavrar_ato_uow import (
    TAtoLavrarAtoUow,
)
from packages.v1.servicos.atos.schemas.t_ato_schema import (
    TAtoLavraturaSchema,
)
from packages.v1.servicos.atos.schemas.t_historico_schema import THistoricoSaveSchema
from packages.v1.servicos.atos.schemas.t_ato_lavrar_ato_uow_schema import (
    TAtoLavrarAtoUowSchema,
)


class FakeBegin:
    def __init__(self, connection):
        self.connection = connection

    def __enter__(self):
        return self.connection

    def __exit__(self, exc_type, exc, tb):
        return False


class FakeEngine:
    def __init__(self, connection):
        self.connection = connection

    def begin(self):
        return FakeBegin(self.connection)


def _lavratura_schema():
    return TAtoLavraturaSchema(
        ato_id=Decimal(10),
        usuario_id=Decimal(1),
        situacao_ato=Decimal(3),
        folha_inicial=Decimal(11),
        folha_final=Decimal(12),
        folha_total=Decimal(2),
        livro_andamento_id=Decimal(7),
        selo_livro_id=Decimal(55),
    )


def _uow_schema():
    return TAtoLavrarAtoUowSchema(
        lavratura=_lavratura_schema(),
        livro_andamento_update=TLivroAndamentoUpdateSchema(
            livro_andamento_id=Decimal(7),
            folha_atual=Decimal(12),
        ),
        caixa_item=CaixaItemSchema(
            caixa_servico_id=4,
            usuario_servico_id=1,
            descricao="Lavratura",
            tabela="T_ATO",
            campo_id=10,
        ),
        selos_update=[
            GSeloLivroUpdateSchema(
                selo_livro_id=55,
                selo_situacao_id=2,
                tabela="T_ATO",
                campo_id=10,
            )
        ],
        historico=THistoricoSaveSchema(
            tabela="T_ATO",
            campo="Lavratura do ato",
            operacao="U",
            usuario_id=1,
            id=10,
        ),
    )


def test_uow_deve_repassar_connection_para_repository_filho(monkeypatch):
    fake_connection = SimpleNamespace(name="transaction-connection")
    calls = []

    def fake_get_engine():
        return FakeEngine(fake_connection)

    def fake_lavrar_execute(self, data, connection=None):
        calls.append(("lavratura", data, connection))
        return {"ato_id": data.ato_id}

    def fake_livro_execute(self, data, connection=None):
        calls.append(("livro", data, connection))
        return SimpleNamespace(livro_andamento_id=data.livro_andamento_id)

    def fake_generate_execute(self, data):
        calls.append(("sequencia", data.tabela, None))
        if data.tabela == "C_CAIXA_ITEM":
            return SimpleNamespace(sequencia=101)
        return SimpleNamespace(sequencia=202)

    def fake_caixa_execute(self, data, connection=None):
        calls.append(("caixa", data, connection))
        return SimpleNamespace(caixa_item_id=data.caixa_item_id)

    def fake_selo_execute(self, data, connection=None):
        calls.append(("selo", data, connection))
        return SimpleNamespace(selo_livro_id=data.selo_livro_id)

    def fake_historico_execute(self, data, connection=None):
        calls.append(("historico", data, connection))
        return SimpleNamespace(historico_id=data.historico_id)

    monkeypatch.setattr(
        "packages.v1.servicos.atos.uow.t_ato.t_ato_lavrar_ato_uow.Firebird.get_engine",
        fake_get_engine,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.uow.t_ato.t_ato_lavrar_ato_uow.TAtoLavrarAtoRepository.execute",
        fake_lavrar_execute,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.uow.t_ato.t_ato_lavrar_ato_uow.TLivroAndamentoUpdateRepository.execute",
        fake_livro_execute,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.uow.t_ato.t_ato_lavrar_ato_uow.GenerateService.execute",
        fake_generate_execute,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.uow.t_ato.t_ato_lavrar_ato_uow.CaixaItemSaveRepository.execute",
        fake_caixa_execute,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.uow.t_ato.t_ato_lavrar_ato_uow.GSeloLivroUpdateRepository.execute",
        fake_selo_execute,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.uow.t_ato.t_ato_lavrar_ato_uow.THistoricoSaveRepository.execute",
        fake_historico_execute,
    )

    data = _uow_schema()
    response = TAtoLavrarAtoUow().execute(data)

    assert response == {"ato_id": Decimal(10)}
    assert [call[0] for call in calls] == [
        "lavratura",
        "livro",
        "sequencia",
        "caixa",
        "selo",
        "sequencia",
        "historico",
    ]
    assert all(call[-1] is fake_connection for call in calls if call[0] != "sequencia")
    assert all(call[-1] is None for call in calls if call[0] == "sequencia")
    assert data.caixa_item.caixa_item_id == 101
    assert data.historico.historico_id == 202


def test_lavrar_ato_repository_deve_funcionar_sem_connection(monkeypatch):
    calls = []

    def fake_run_and_return(self, sql, params=None, connection=None):
        calls.append(
            {
                "sql": sql,
                "params": params,
                "connection": connection,
            }
        )
        return {"ato_id": params["ato_id"]}

    monkeypatch.setattr(
        "abstracts.repository.BaseRepository.run_and_return",
        fake_run_and_return,
    )

    data = _lavratura_schema()
    response = TAtoLavrarAtoRepository().execute(data)

    assert response == {"ato_id": Decimal(10)}
    assert len(calls) == 1
    assert calls[0]["connection"] is None
    assert calls[0]["params"]["ato_id"] == Decimal(10)
