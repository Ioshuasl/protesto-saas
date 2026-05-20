from decimal import Decimal
import sys
import types
from types import SimpleNamespace

import pytest
from fastapi import HTTPException

sys.modules.setdefault("fitz", types.SimpleNamespace())

from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoLavraturaSchema
from packages.v1.servicos.atos.services.t_ato.go.t_ato_lavrar_ato_service import (
    TAtoLavrarAtoService,
)


def test_deve_lavrar_ato_gerando_selo(monkeypatch):
    def fake_ato_show(self, data):
        return SimpleNamespace(ato_id=data.ato_id, ato_tipo_id=5, protocolo=123, selo_livro_id=None, ato_antigo="N")

    def fake_selo_existente(self, data):
        assert data.tabela == "T_ATO"
        assert data.campo_id == 10
        return None

    def fake_ato_tipo_show(self, data):
        return SimpleNamespace(
            livro_natureza_id=2,
            descricao="Escritura",
            possui_imovel="N",
            possui_ato_anterior="N",
        )

    def fake_livro_natureza_show(self, data):
        return SimpleNamespace(livro_natureza_id=data.livro_natureza_id, frente_verso="N")

    def fake_livro_andamento_show(self, data):
        return SimpleNamespace(livro_andamento_id=7, folha_atual=Decimal(10))

    def fake_display_texto(self, data):
        return SimpleNamespace(texto="ato.docx")

    def fake_convert_to_pdf(**kwargs):
        assert kwargs["input_docx_path"] == "storage/temp/ato.docx"
        return {"pages": 2}

    def fake_vinculo_valor_index(self, data):
        return [
            SimpleNamespace(
                ato_id=10,
                selo_grupo_id=9,
                emol_principal="S",
                emolumento=Decimal("100"),
                taxa_judiciaria=Decimal("10"),
                fundesp=Decimal("5"),
                valor_iss=Decimal("2"),
                valor_total=Decimal("115"),
                emolumento_item_id=99,
            )
        ]

    def fake_vinculo_parte_index(self, data):
        return [
            SimpleNamespace(
                requerente="S",
                pessoa_nome="Joao da Silva",
                pessoa_cpf="12345678900",
            )
        ]

    def fake_selo_livre_show(self, data):
        assert data.selo_grupo_id == 9
        return SimpleNamespace(selo_livro_id=55, numero_selo="A00055")

    def fake_selo_update(self, data):
        assert data.selo_livro_id == 55
        assert data.selo_situacao_id == 2
        assert data.tabela == "T_ATO"
        assert data.campo_id == 10
        assert data.valor_total == Decimal("115")
        assert data.emolumento_item_id == 99
        return SimpleNamespace(selo_livro_id=data.selo_livro_id)

    def fake_lavrar_transaction(self, data):
        assert data.lavratura.situacao_ato == 3
        assert data.lavratura.folha_inicial == Decimal(11)
        assert data.lavratura.folha_final == Decimal(12)
        assert data.lavratura.folha_total == Decimal(2)
        assert data.lavratura.livro_andamento_id == 7
        assert data.lavratura.selo_livro_id == Decimal(55)
        assert data.livro_andamento_update.livro_andamento_id == 7
        assert data.livro_andamento_update.folha_atual == Decimal(12)
        assert data.caixa_item.descricao == "Prot.:123 - Escritura - Joao da Silva"
        assert data.caixa_item.valor_servico == 117
        assert len(data.selos_update) == 1
        assert data.selos_update[0].selo_livro_id == 55
        assert data.historico.tabela == "T_ATO"
        assert data.ato_anterior_update is None
        return {"ato_id": data.lavratura.ato_id}

    def fake_livro_andamento_update(self, data):
        assert data.livro_andamento_id == 7
        assert data.folha_atual == Decimal(12)
        return SimpleNamespace(livro_andamento_id=data.livro_andamento_id)

    def fake_caixa_item_save(self, data):
        assert data.especie_pagamento == "D"
        assert data.caixa_servico_id == 4
        assert data.apresentante == "Joao da Silva"
        assert data.usuario_servico_id == 1
        assert data.chave_servico == 10
        assert data.descricao == "Prot.:123 - Escritura - Joao da Silva"
        assert data.situacao == 4
        assert data.tipo_documento == "C"
        assert data.tipo_transacao == "C"
        assert data.tipo_servico == "1"
        assert data.registrado == 1
        assert data.emolumento_item_id is None
        assert data.emolumento == Decimal("100")
        assert data.taxa_judiciaria == Decimal("10")
        assert data.iss == Decimal("2")
        assert data.fundesp is None
        assert data.fundo_ri == Decimal("5")
        assert data.desconto == 0
        assert data.outra_taxa1 == 0
        assert data.valor_taxa == Decimal(0)
        assert data.cpfcnpj_apresentante == "12345678900"
        assert data.nome_pagador == "Joao da Silva"
        assert data.valor_servico == 117
        assert data.valor_pago == Decimal("117")
        assert data.tabela == "T_ATO"
        assert data.campo_id == 10
        return SimpleNamespace(caixa_item_id=1)

    def fake_historico_save(self, data):
        return SimpleNamespace(historico_id=1)

    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_lavrar_ato_service.TAtoShowAction.execute",
        fake_ato_show,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_lavrar_ato_service.GSeloLivroShowByTabelaCampoRepository.execute",
        fake_selo_existente,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_lavrar_ato_service.TAtoTipoShowAction.execute",
        fake_ato_tipo_show,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_lavrar_ato_service.TLivroNaturezaShowAction.execute",
        fake_livro_natureza_show,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_lavrar_ato_service.TLivroAndamentoFirstAbertoByNaturezaAction.execute",
        fake_livro_andamento_show,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_lavrar_ato_service.TAtoDisplayTextoService.execute",
        fake_display_texto,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_lavrar_ato_service.DOCXConvertToPDFAction.execute",
        fake_convert_to_pdf,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_lavrar_ato_service.TAtoVinculoValorIndexAction.execute",
        fake_vinculo_valor_index,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_lavrar_ato_service.TAtoVinculoParteIndexAction.execute",
        fake_vinculo_parte_index,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_lavrar_ato_service.GSeloLivroLivreShowService.execute",
        fake_selo_livre_show,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_lavrar_ato_service.TAtoLavrarAtoUowAction.execute",
        fake_lavrar_transaction,
    )

    data = TAtoLavraturaSchema(ato_id=10, usuario_id=1)
    response = TAtoLavrarAtoService().execute(data)

    assert response == {"ato_id": 10}


def test_deve_retornar_422_quando_ato_nao_tem_valores_para_selo(monkeypatch):
    def fake_ato_show(self, data):
        return SimpleNamespace(ato_id=data.ato_id, ato_tipo_id=5, protocolo=123, selo_livro_id=None, ato_antigo="N")

    def fake_selo_existente(self, data):
        return None

    def fake_ato_tipo_show(self, data):
        return SimpleNamespace(livro_natureza_id=2, descricao="Escritura", possui_imovel="N")

    def fake_livro_natureza_show(self, data):
        return SimpleNamespace(livro_natureza_id=data.livro_natureza_id, frente_verso="N")

    def fake_livro_andamento_show(self, data):
        return SimpleNamespace(livro_andamento_id=7, folha_atual=Decimal(10))

    def fake_display_texto(self, data):
        return SimpleNamespace(texto="ato.docx")

    def fake_convert_to_pdf(**kwargs):
        return {"pages": 2}

    def fake_vinculo_valor_index(self, data):
        return []

    def fake_vinculo_parte_index(self, data):
        return [
            SimpleNamespace(
                requerente="S",
                pessoa_nome="Joao da Silva",
            )
        ]

    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_lavrar_ato_service.TAtoShowAction.execute",
        fake_ato_show,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_lavrar_ato_service.GSeloLivroShowByTabelaCampoRepository.execute",
        fake_selo_existente,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_lavrar_ato_service.TAtoTipoShowAction.execute",
        fake_ato_tipo_show,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_lavrar_ato_service.TLivroNaturezaShowAction.execute",
        fake_livro_natureza_show,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_lavrar_ato_service.TLivroAndamentoFirstAbertoByNaturezaAction.execute",
        fake_livro_andamento_show,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_lavrar_ato_service.TAtoDisplayTextoService.execute",
        fake_display_texto,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_lavrar_ato_service.DOCXConvertToPDFAction.execute",
        fake_convert_to_pdf,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_lavrar_ato_service.TAtoVinculoValorIndexAction.execute",
        fake_vinculo_valor_index,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_lavrar_ato_service.TAtoVinculoParteIndexAction.execute",
        fake_vinculo_parte_index,
    )

    data = TAtoLavraturaSchema(ato_id=10, usuario_id=1)

    with pytest.raises(HTTPException) as exc:
        TAtoLavrarAtoService().execute(data)

    assert exc.value.status_code == 422
    assert exc.value.detail == "[TA412] Valores vinculados ao ato nao encontrados."


def test_deve_bloquear_lavratura_quando_ato_ja_tem_selo():
    def fake_ato_show(self, data):
        return SimpleNamespace(
            ato_id=data.ato_id,
            ato_tipo_id=5,
            protocolo=123,
            selo_livro_id=55,
            ato_antigo="N",
        )

    from packages.v1.servicos.atos.services.t_ato.go import t_ato_lavrar_ato_service

    original_execute = t_ato_lavrar_ato_service.TAtoShowAction.execute
    t_ato_lavrar_ato_service.TAtoShowAction.execute = fake_ato_show

    data = TAtoLavraturaSchema(ato_id=10, usuario_id=1)

    try:
        with pytest.raises(HTTPException) as exc:
            TAtoLavrarAtoService().execute(data)
    finally:
        t_ato_lavrar_ato_service.TAtoShowAction.execute = original_execute

    assert exc.value.status_code == 409
    assert exc.value.detail == "[TA423] Ato ja possui selo ou agrupador vinculado. Lavratura bloqueada."


def test_deve_bloquear_lavratura_quando_existe_agrupador_vinculado(monkeypatch):
    def fake_ato_show(self, data):
        return SimpleNamespace(
            ato_id=data.ato_id,
            ato_tipo_id=5,
            protocolo=123,
            selo_livro_id=None,
            ato_antigo="N",
        )

    def fake_selo_existente(self, data):
        assert data.tabela == "T_ATO"
        assert data.campo_id == 10
        return SimpleNamespace(
            selo_livro_id=55,
            numero_agrupador="A00055",
        )

    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_lavrar_ato_service.TAtoShowAction.execute",
        fake_ato_show,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_lavrar_ato_service.GSeloLivroShowByTabelaCampoRepository.execute",
        fake_selo_existente,
    )

    data = TAtoLavraturaSchema(ato_id=10, usuario_id=1)

    with pytest.raises(HTTPException) as exc:
        TAtoLavrarAtoService().execute(data)

    assert exc.value.status_code == 409
    assert exc.value.detail == "[TA423] Ato ja possui selo ou agrupador vinculado. Lavratura bloqueada."


def test_deve_bloquear_lavratura_quando_tipo_exige_imovel_e_ato_nao_tem_imovel(monkeypatch):
    def fake_ato_show(self, data):
        return SimpleNamespace(
            ato_id=data.ato_id,
            ato_tipo_id=5,
            protocolo=123,
            selo_livro_id=None,
            ato_antigo="N",
        )

    def fake_selo_existente(self, data):
        return None

    def fake_ato_tipo_show(self, data):
        return SimpleNamespace(
            livro_natureza_id=2,
            descricao="Escritura",
            possui_imovel="S",
        )

    def fake_vinculo_imovel_index(self, data):
        assert data.ato_id == 10
        return []

    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_lavrar_ato_service.TAtoShowAction.execute",
        fake_ato_show,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_lavrar_ato_service.GSeloLivroShowByTabelaCampoRepository.execute",
        fake_selo_existente,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_lavrar_ato_service.TAtoTipoShowAction.execute",
        fake_ato_tipo_show,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_lavrar_ato_service.TAtoVinculoImovelIndexAction.execute",
        fake_vinculo_imovel_index,
    )

    data = TAtoLavraturaSchema(ato_id=10, usuario_id=1)

    with pytest.raises(HTTPException) as exc:
        TAtoLavrarAtoService().execute(data)

    assert exc.value.status_code == 422
    assert exc.value.detail == "[TA424] Tipo de ato exige imovel, mas nao existe imovel vinculado ao ato."


def test_deve_ignorar_imovel_obrigatorio_quando_ato_for_antigo(monkeypatch):
    def fake_ato_show(self, data):
        return SimpleNamespace(ato_id=data.ato_id, ato_tipo_id=5, protocolo=123, selo_livro_id=None, ato_antigo="S")

    def fake_selo_existente(self, data):
        return None

    def fake_ato_tipo_show(self, data):
        return SimpleNamespace(livro_natureza_id=2, descricao="Escritura", possui_imovel="S")

    def fake_livro_natureza_show(self, data):
        return SimpleNamespace(livro_natureza_id=data.livro_natureza_id, frente_verso="N")

    def fake_livro_andamento_show(self, data):
        return SimpleNamespace(livro_andamento_id=7, folha_atual=Decimal(10))

    def fake_display_texto(self, data):
        return SimpleNamespace(texto="ato.docx")

    def fake_convert_to_pdf(**kwargs):
        return {"pages": 2}

    def fake_vinculo_valor_index(self, data):
        return []

    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_lavrar_ato_service.TAtoShowAction.execute",
        fake_ato_show,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_lavrar_ato_service.GSeloLivroShowByTabelaCampoRepository.execute",
        fake_selo_existente,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_lavrar_ato_service.TAtoTipoShowAction.execute",
        fake_ato_tipo_show,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_lavrar_ato_service.TLivroNaturezaShowAction.execute",
        fake_livro_natureza_show,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_lavrar_ato_service.TLivroAndamentoFirstAbertoByNaturezaAction.execute",
        fake_livro_andamento_show,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_lavrar_ato_service.TAtoDisplayTextoService.execute",
        fake_display_texto,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_lavrar_ato_service.DOCXConvertToPDFAction.execute",
        fake_convert_to_pdf,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_lavrar_ato_service.TAtoVinculoValorIndexAction.execute",
        fake_vinculo_valor_index,
    )

    data = TAtoLavraturaSchema(ato_id=10, usuario_id=1)

    with pytest.raises(HTTPException) as exc:
        TAtoLavrarAtoService().execute(data)

    assert exc.value.status_code == 422
    assert exc.value.detail == "[TA412] Valores vinculados ao ato nao encontrados."


def test_deve_bloquear_lavratura_quando_doi_obrigatoria_sem_vinculo_parte_imovel(monkeypatch):
    def fake_ato_show(self, data):
        return SimpleNamespace(ato_id=data.ato_id, ato_tipo_id=5, protocolo=123, selo_livro_id=None, ato_antigo="N")

    def fake_selo_existente(self, data):
        return None

    def fake_ato_tipo_show(self, data):
        return SimpleNamespace(
            livro_natureza_id=2,
            descricao="Escritura",
            possui_imovel="N",
            informar_doi="S",
        )

    def fake_livro_natureza_show(self, data):
        return SimpleNamespace(livro_natureza_id=data.livro_natureza_id, frente_verso="N")

    def fake_livro_andamento_show(self, data):
        return SimpleNamespace(livro_andamento_id=7, folha_atual=Decimal(10))

    def fake_display_texto(self, data):
        return SimpleNamespace(texto="ato.docx")

    def fake_convert_to_pdf(**kwargs):
        return {"pages": 2}

    def fake_vinculo_valor_index(self, data):
        return [
            SimpleNamespace(
                ato_id=10,
                selo_grupo_id=9,
                emolumento=Decimal("100"),
                taxa_judiciaria=Decimal("10"),
                fundesp=Decimal("5"),
                valor_iss=Decimal("2"),
                emolumento_item_id=99,
            )
        ]

    def fake_vinculo_parte_index(self, data):
        return [
            SimpleNamespace(
                requerente="S",
                pessoa_nome="Joao da Silva",
            )
        ]

    def fake_parte_imovel_index(self, data):
        assert data.ato_id == 10
        return []

    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_lavrar_ato_service.TAtoShowAction.execute",
        fake_ato_show,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_lavrar_ato_service.GSeloLivroShowByTabelaCampoRepository.execute",
        fake_selo_existente,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_lavrar_ato_service.TAtoTipoShowAction.execute",
        fake_ato_tipo_show,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_lavrar_ato_service.TLivroNaturezaShowAction.execute",
        fake_livro_natureza_show,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_lavrar_ato_service.TLivroAndamentoFirstAbertoByNaturezaAction.execute",
        fake_livro_andamento_show,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_lavrar_ato_service.TAtoDisplayTextoService.execute",
        fake_display_texto,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_lavrar_ato_service.DOCXConvertToPDFAction.execute",
        fake_convert_to_pdf,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_lavrar_ato_service.TAtoVinculoValorIndexAction.execute",
        fake_vinculo_valor_index,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_lavrar_ato_service.TAtoVinculoParteIndexAction.execute",
        fake_vinculo_parte_index,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato.go.t_ato_lavrar_ato_service.TAtoParteImovelIndexAction.execute",
        fake_parte_imovel_index,
    )

    data = TAtoLavraturaSchema(ato_id=10, usuario_id=1)

    with pytest.raises(HTTPException) as exc:
        TAtoLavrarAtoService().execute(data)

    assert exc.value.status_code == 422
    assert exc.value.detail == "[TA425] DOI obrigatoria, mas nao existe vinculo valido entre parte e imovel."
