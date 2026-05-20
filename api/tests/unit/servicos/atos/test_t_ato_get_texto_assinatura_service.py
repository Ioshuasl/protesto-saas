from types import SimpleNamespace

from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoTextoAssinatura
from packages.v1.servicos.atos.services.t_ato.go.t_ato_get_texto_assinatura_service import (
    TAtoGetTextoAssinaturaService,
)


def test_nao_deve_quebrar_quando_houver_parte_com_assinatura_tipo_invalido(monkeypatch):
    def fake_get_texto_assinatura(self, data):
        return SimpleNamespace(ato_id=data.ato_id, texto_assinatura=None)

    def fake_index_partes(self, data):
        return [SimpleNamespace(assinatura_tipo=99, ato_vinculoparte_id=10)]

    def should_not_be_called(*args, **kwargs):
        raise AssertionError("Nao deveria executar merge/resolver para tipo invalido")

    def fake_docx_process(self, data):
        return "ato_assinatura_merge_arquivo.docx"

    monkeypatch.setattr(
        "packages.v1.servicos.atos.actions.t_ato.t_ato_get_texto_assinatura_action.TAtoGetTextoAssinaturaAction.execute",
        fake_get_texto_assinatura,
    )
    monkeypatch.setattr(
        "packages.v1.servicos.atos.services.t_ato_vinculoparte.go.t_ato_vinculoparte_index_service.TAtoVinculoParteIndexService.execute",
        fake_index_partes,
    )
    monkeypatch.setattr(
        "packages.v1.resolver.services.resolver_main_service.ResolverMainService.execute",
        should_not_be_called,
    )
    monkeypatch.setattr(
        "packages.v1.docx.services.docx_merge_modelo_minuta_service.DOCXMergeModeloMinutaService.execute",
        should_not_be_called,
    )
    monkeypatch.setattr(
        "packages.v1.docx.services.docx_process_service.DOCXProcess.execute",
        fake_docx_process,
    )

    response = TAtoGetTextoAssinaturaService().execute(
        TAtoTextoAssinatura(ato_id=1, tipo_assinatura=1)
    )

    assert response.texto_assinatura == "ato_assinatura_merge_arquivo.docx"
