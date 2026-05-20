import base64
from packages.v1.docx.services.docx_merge_modelo_minuta_service import (
    DOCXMergeModeloMinutaService,
)
from packages.v1.docx.services.docx_process_service import DOCXProcess, DOCXProcessSchema
from packages.v1.servicos.atos.actions.t_ato_vinculoparte.t_ato_vinculoparte_index_action import TAtoVinculoParteIndexAction
from packages.v1.servicos.atos.actions.t_ato_vinculoparte.t_ato_vinculoparte_index_by_tipo_vinculo_action import TAtoVinculoParteIndexByTipoVinculoAction
from packages.v1.servicos.atos.schemas.t_ato_vinculoparte_schema import TAtoVinculoParteIndexByTipoVinculoSchema, TAtoVinculoParteIndexSchema


class ResolverAtoOutorganteQualificacao:

    @staticmethod
    def execute(data: object):

        # Busca todas as partes vinculadas
        response_ato_vinculo_parte = TAtoVinculoParteIndexByTipoVinculoAction().execute(
            TAtoVinculoParteIndexByTipoVinculoSchema(
                ato_id=data.texto.campo_id_valor,
                tipo_vinculo=1
            )
        )

        merge_service = DOCXMergeModeloMinutaService()
        process_service = DOCXProcess()
        merged_docx = None

        for ato_parte in response_ato_vinculo_parte:
            raw_qualificacao = getattr(ato_parte, "texto_qualificacao", None)
            if not raw_qualificacao:
                continue

            qualificacao_docx = base64.b64decode(raw_qualificacao)

            if merged_docx is None:
                merged_docx = qualificacao_docx
                continue

            merged_docx = merge_service.execute(
                modelo_content=merged_docx,
                minuta_content=qualificacao_docx,
                output="binary",
            )

        if not merged_docx:
            return ""

        # Retorna apenas o conteúdo textual do body do DOCX mesclado.
        response_text = process_service.execute(
            DOCXProcessSchema(
                id=f"ato_{data.texto.campo_id_valor}_outorgante_qualificacao",
                content=merged_docx,
                output="txt",
            )
        )
        return " ".join(str(response_text or "").split())
