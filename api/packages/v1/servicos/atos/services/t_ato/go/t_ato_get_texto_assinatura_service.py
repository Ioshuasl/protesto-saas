from fastapi import HTTPException, status
from packages.v1.administrativo.actions.g_marcacao_tipo.g_marcacao_tipo_show_action import GMarcacaoTipoShowAction
from packages.v1.administrativo.schemas.g_marcacao_tipo_schema import GMarcacaoTipoIdSchema
from packages.v1.administrativo.schemas.t_livro_natureza_schema import TLivroNaturezaIdSchema
from packages.v1.parametros.schemas.g_config_schema import GConfigShowByBreadcumbSchema
from packages.v1.docx.services.docx_merge_modelo_minuta_service import (
    DOCXMergeModeloMinutaService,
)
from packages.v1.docx.services.docx_process_service import DOCXProcess, DOCXProcessSchema
from packages.v1.resolver.actions.lista.resolver_cartorio_cidade_action import GConfigShowByBreadcumbAction
from packages.v1.resolver.schemas.resolver_schema import ResolverSchema
from packages.v1.resolver.services.resolver_main_service import ResolverMainService
from packages.v1.servicos.atos.actions.t_ato.t_ato_get_texto_assinatura_action import (
    TAtoGetTextoAssinaturaAction,
)
from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoIdSchema, TAtoTextoAssinatura
from packages.v1.servicos.atos.schemas.t_ato_tipo_schema import TAtoTipoIdSchema
from packages.v1.servicos.atos.schemas.t_ato_vinculoparte_schema import TAtoVinculoParteIndexSchema
from packages.v1.servicos.atos.services.t_ato.go.t_ato_show_service import TAtoShowService
from packages.v1.servicos.atos.services.t_ato_vinculoparte.go.t_ato_vinculoparte_index_service import TAtoVinculoParteIndexService


class TAtoGetTextoAssinaturaService:

    """
    Servico responsavel por buscar e resolver o texto de assinatura do ato.
    """

    def execute(self, data: TAtoTextoAssinatura):

        if data.tipo_assinatura == 1:

            data.coluna = 'texto_assinatura'

        if data.tipo_assinatura == 2:

            data.coluna = 'texto_assinatura_traslado'

        response_assinatura = TAtoGetTextoAssinaturaAction().execute(data)

        if not response_assinatura:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nao encontramos o ato informado. Verifique o codigo e tente novamente.",
            )

        if not response_assinatura.texto_assinatura:

            #  Normaliza a assinatura
            response_assinatura.texto_assinatura = ""

            response_ato_parte = TAtoVinculoParteIndexService().execute(
                TAtoVinculoParteIndexSchema(
                    ato_id=data.ato_id
                )
            )

            if not response_ato_parte:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Nao encontramos as partes do ato para montar as assinaturas.",
                )

            for ato_parte in response_ato_parte:
                reponse_marcacao_tipo = None

                if int(ato_parte.assinatura_tipo) == 1:

                    response_config = GConfigShowByBreadcumbAction().execute(GConfigShowByBreadcumbSchema(
                                grupo_descricao="SAAS",
                                secao="ATO",
                                nome="MODELO_ASSINATURA_NORMAL",
                                sistema_id=2,
                            )
                        )

                    if not response_config:
                        raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail="Nao encontramos configuracao de assinatura para este ato.",
                        )

                    if response_config.valor in (None, ""):
                        continue

                    reponse_marcacao_tipo = GMarcacaoTipoShowAction().execute(
                         GMarcacaoTipoIdSchema(
                            marcacao_tipo_id=response_config.valor,
                        )
                    )

                if int(ato_parte.assinatura_tipo) == 2:

                    response_config = GConfigShowByBreadcumbAction().execute(GConfigShowByBreadcumbSchema(
                                grupo_descricao="SAAS",
                                secao="ATO",
                                nome="MODELO_ASSINATURA_PELA_DIGITAL",
                                sistema_id=2,
                            )
                        )

                    if not response_config:
                        raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail="Nao encontramos configuracao de assinatura para este ato.",
                        )

                    if response_config.valor in (None, ""):
                        continue

                    reponse_marcacao_tipo = GMarcacaoTipoShowAction().execute(
                         GMarcacaoTipoIdSchema(
                            marcacao_tipo_id=response_config.valor,
                        )
                    )

                if int(ato_parte.assinatura_tipo) == 3:

                    response_config = GConfigShowByBreadcumbAction().execute(GConfigShowByBreadcumbSchema(
                                grupo_descricao="SAAS",
                                secao="ATO",
                                nome="MODELO_ASSINATURA_DIGITAL",
                                sistema_id=2,
                            )
                        )

                    if not response_config:
                        raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail="Nao encontramos configuracao de assinatura para este ato.",
                        )

                    if response_config.valor in (None, ""):
                        continue

                    reponse_marcacao_tipo = GMarcacaoTipoShowAction().execute(
                         GMarcacaoTipoIdSchema(
                            marcacao_tipo_id=response_config.valor,
                        )
                    )

                # Qualificação da assinatura
                if not reponse_marcacao_tipo:
                    continue

                ato_parte.texto_assinatura = ResolverMainService().execute(
                    ResolverSchema(
                        id=ato_parte.ato_vinculoparte_id,
                        campo_id_valor=ato_parte.ato_vinculoparte_id,
                        sitema_id=2,
                        texto=reponse_marcacao_tipo.texto,
                    )
                )

                # Merge das assinaturas
                response_assinatura.texto_assinatura = DOCXMergeModeloMinutaService().execute(
                        modelo_content=ato_parte.texto_assinatura,
                        minuta_content=response_assinatura.texto_assinatura,
                        output="binary",
                    )

        response_assinatura.texto_assinatura = DOCXProcess().execute(
                DOCXProcessSchema(
                    id=f"{response_assinatura.ato_id}_assinatura_merge",
                    content=response_assinatura.texto_assinatura,
                    output="path",
                    save_disk=True,
                    storage_dir="./storage/temp",
                    filename_prefix="ato_assinatura_merge",
                )
            )


        return response_assinatura
