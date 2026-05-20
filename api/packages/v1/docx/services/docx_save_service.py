from actions.data.text import Text
from packages.v1.administrativo.controllers.g_marcacao_tipo_controller import (
    GMarcacaoTipoUpdateService,
)
from packages.v1.administrativo.schemas.g_marcacao_tipo_schema import (
    GMarcacaoTipoUpdateSchema,
)
from packages.v1.administrativo.schemas.t_livro_natureza_schema import TLivroNaturezaUpdateModeloSchema
from packages.v1.administrativo.schemas.t_minuta_schema import TMinutaUpdateTextoSchema
from packages.v1.administrativo.services.t_livro_natureza.go.t_livro_natureza_update_modelo_texto_service import TLivroNaturezaUpdateModeloTextoService
from packages.v1.administrativo.services.t_minuta.go.t_minuta_update_texto_service import TMinutaUpdateTextoService
from packages.v1.docx.actions.docx_load_only_office_file_bytes_action import DOCXLoadOnlyOfficeFileBytesAction
from packages.v1.docx.schemas.docx_schema import DOCXSchemaCallback
from packages.v1.parametros.schemas.g_config_schema import (
    GConfigSaveSchema,
)
from packages.v1.parametros.services.g_config.go.g_config_save_service import (
    GConfigSaveService,
)
from packages.v1.servicos.atos.schemas.t_ato_schema import (
    TAtoTextoAssinaturaUpdateSchema,
    TAtoTextoFinalizacaoUpdateSchema,
    TAtoUpdateTextoSchema,
)
from packages.v1.servicos.atos.schemas.t_ato_vinculoparte_schema import (
    TAtoVinculoParteTextoQualificacaoUpdateSchema,
)
from packages.v1.servicos.atos.services.t_ato.go.t_ato_update_texto_assinatura_service import (
    TAtoUpdateTextoAssinaturaService,
)
from packages.v1.servicos.atos.services.t_ato.go.t_ato_update_texto_finalizacao_service import TAtoUpdateTextoFinalizacaoService
from packages.v1.servicos.atos.services.t_ato.go.t_ato_update_texto_service import TAtoUpdateTextoService
from packages.v1.servicos.atos.services.t_ato_vinculoparte.go.t_ato_vinculoparte_update_texto_qualificacao_service import (
    TAtoVinculoParteUpdateTextoQualificacaoService,
)



class DOCXSaveService:

    def execute(self, data: DOCXSchemaCallback):

        response = None

        # OnlyOffice envia status 2 ou 6 quando deve salvar
        status = data.data.get("status")

        if status not in (2, 6):
            return {"error": 0}

        file_content = DOCXLoadOnlyOfficeFileBytesAction.execute(data)
        file_content_bytes = Text.compress(file_content)

        if data.servico == "g_marcacao_tipo_update_service":

            response = GMarcacaoTipoUpdateService().execute(
                GMarcacaoTipoUpdateSchema(
                    marcacao_tipo_id=data.registro_id,
                    texto=file_content_bytes,  # ou base64 se preferir
                )
            )

        if data.servico == "g_config_update_service":

            response = GConfigSaveService().execute(
                GConfigSaveSchema(
                    config_id=data.registro_id,
                    texto=file_content_bytes
                )
            )

        if data.servico == "t_minuta_update_service":

            response = TMinutaUpdateTextoService().execute(
                TMinutaUpdateTextoSchema(
                    minuta_id=data.registro_id,
                    texto=file_content_bytes
                )
            )

        if data.servico == "t_ato_update_texto_service":

            response = TAtoUpdateTextoService().execute(
                TAtoUpdateTextoSchema(
                    ato_id=data.registro_id,
                    texto=file_content_bytes
                )
            )

        if data.servico == "t_ato_update_texto_finalizacao_livro_service":

            response = TAtoUpdateTextoFinalizacaoService().execute(
                TAtoTextoFinalizacaoUpdateSchema(
                    ato_id=data.registro_id,
                    tipo_finalizacao=1,
                    coluna='texto_finalizacao',
                    texto=file_content_bytes
                )
            )

        if data.servico == "t_ato_update_texto_finalizacao_traslado_service":

            response = TAtoUpdateTextoFinalizacaoService().execute(
                TAtoTextoFinalizacaoUpdateSchema(
                    ato_id=data.registro_id,
                    tipo_finalizacao=2,
                    coluna='texto_finalizacao_traslado',
                    texto=file_content_bytes
                )
            )

        if data.servico == "t_ato_update_texto_assinatura_livro_service":

            response = TAtoUpdateTextoAssinaturaService().execute(
                TAtoTextoAssinaturaUpdateSchema(
                    ato_id=data.registro_id,
                    tipo_assinatura=1,
                    coluna='texto_assinatura',
                    texto=file_content_bytes
                )
            )

        if data.servico == "t_ato_update_texto_assinatura_traslado_service":

            response = TAtoUpdateTextoAssinaturaService().execute(
                TAtoTextoAssinaturaUpdateSchema(
                    ato_id=data.registro_id,
                    tipo_assinatura=2,
                    coluna='texto_assinatura_traslado',
                    texto=file_content_bytes
                )
            )

        if data.servico == "t_livro_natureza_update_modelo_livro_service":

            response = TLivroNaturezaUpdateModeloTextoService().execute(
                TLivroNaturezaUpdateModeloSchema(
                    livro_natureza_id=data.registro_id,
                    modelo_texto=file_content_bytes,
                    coluna='modelo_livro'
                )
            )

        if data.servico == "t_livro_natureza_update_modelo_traslado_service":

            response = TLivroNaturezaUpdateModeloTextoService().execute(
                TLivroNaturezaUpdateModeloSchema(
                    livro_natureza_id=data.registro_id,
                    modelo_texto=file_content_bytes,
                    coluna='modelo_traslado'
                )
            )

        if data.servico == "t_livro_natureza_update_modelo_livro_pdf_service":

            response = TLivroNaturezaUpdateModeloTextoService().execute(
                TLivroNaturezaUpdateModeloSchema(
                    livro_natureza_id=data.registro_id,
                    modelo_texto=file_content_bytes,
                    coluna='modelo_livro_pdf',
                )
            )

        if data.servico == "t_livro_natureza_update_modelo_traslado_pdf_service":

            response = TLivroNaturezaUpdateModeloTextoService().execute(
                TLivroNaturezaUpdateModeloSchema(
                    livro_natureza_id=data.registro_id,
                    modelo_texto=file_content_bytes,
                    coluna='modelo_traslado_pdf',
                )
            )

        if data.servico == "t_ato_vinculoparte_update_texto_qualificacao_service":

            response = TAtoVinculoParteUpdateTextoQualificacaoService().execute(
                TAtoVinculoParteTextoQualificacaoUpdateSchema(
                    ato_vinculoparte_id=data.registro_id,
                    texto_qualificacao=file_content_bytes,
                )
            )


        return response
