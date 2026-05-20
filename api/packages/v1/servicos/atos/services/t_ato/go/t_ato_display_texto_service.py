from packages.v1.administrativo.actions.t_livro_natureza.t_livro_natureza_show_modelo_action import TLivroNaturezaShowModeloAction
from packages.v1.administrativo.controllers.t_livro_natureza_controller import TLivroNaturezaShowModeloService
from packages.v1.administrativo.schemas.t_livro_natureza_schema import TLivroNaturezaShowModeloSchema
from packages.v1.docx.services.docx_process_service import DOCXProcess, DOCXProcessSchema
from packages.v1.docx.services.docx_merge_modelo_minuta_service import DOCXMergeModeloMinutaService
from packages.v1.servicos.atos.actions.t_ato.t_ato_get_texto_assinatura_action import TAtoGetTextoAssinaturaAction
from packages.v1.servicos.atos.actions.t_ato.t_ato_get_texto_corpo_action import TAtoGetTextoCorpoAction
from packages.v1.servicos.atos.actions.t_ato.t_ato_get_texto_finalizacao_action import TAtoGetTextoFinalizacaoAction
from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoTextoAssinatura, TAtoTextoFinalizacao, TAtoTextoVisualizarSchema
from fastapi import HTTPException, status


class TAtoDisplayTextoService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela T_ATO.
    """

    def execute(self, data: TAtoTextoVisualizarSchema):

        response_ato = TAtoGetTextoCorpoAction().execute(data)

        if not response_ato:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nao encontramos o ato informado. Verifique o codigo e tente novamente.",
            )

        # Schema do livro natureza
        t_livro_natureza_show_modelo_schema = TLivroNaturezaShowModeloSchema(
            livro_natureza_id = response_ato.livro_natureza_id
        )

        # Schema da finalização do ato
        t_ato_finalizacao_schema = TAtoTextoFinalizacao(
                ato_id=response_ato.ato_id,
                tipo_finalizacao=data.tipo_visualizacao,
            )

        # Schema do texto de assinatura
        t_ato_texto_assinatura_schema = TAtoTextoAssinatura(
                ato_id=response_ato.ato_id,
                tipo_assinatura=data.tipo_visualizacao,
            )

        match data.tipo_visualizacao:

            #  Definições do livro
            case 1:
                t_livro_natureza_show_modelo_schema.coluna = 'MODELO_LIVRO'
                t_ato_finalizacao_schema.coluna = 'texto_finalizacao'
                t_ato_texto_assinatura_schema.coluna = 'texto_assinatura'

            # Definições do traslado
            case 2:
                t_livro_natureza_show_modelo_schema.coluna = 'MODELO_TRASLADO'
                t_ato_finalizacao_schema.coluna = 'texto_finalizacao_traslado'
                t_ato_texto_assinatura_schema.coluna = 'texto_assinatura_traslado'

            case _:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Informe um tipo de visualizacao valido para gerar o texto.",
                )

        # Busca o modelo de acordo com o livro natureza
        response_livro_natureza = TLivroNaturezaShowModeloAction().execute(t_livro_natureza_show_modelo_schema)

        if not response_livro_natureza:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nao encontramos a configuracao de livro para este ato.",
            )

        # Modelo do ato
        modelo_docx = DOCXProcess().execute(
            DOCXProcessSchema(
                id=f"{response_ato.ato_id}_modelo",
                content=response_livro_natureza.modelo_texto,
                output="binary",
            )
        )

        # Texto do ato
        corpo_docx = DOCXProcess().execute(
            DOCXProcessSchema(
                id=f"{response_ato.ato_id}_texto_corpo",
                content=response_ato.texto,
                output="binary",
            )
        )

        # Merge do ato com o modelo definido
        response_ato.texto = DOCXMergeModeloMinutaService().execute(
            modelo_content=modelo_docx,
            minuta_content=corpo_docx,
            output="binary"
        )

        # Busca o texto da finalização
        response_ato_finalizacao = TAtoGetTextoFinalizacaoAction().execute(t_ato_finalizacao_schema)

        if not response_ato_finalizacao:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nao encontramos o texto de finalizacao para este ato.",
            )

        # Monta o docx da finalização
        finalizacao_docx = DOCXProcess().execute(
            DOCXProcessSchema(
                id=f"{response_ato.ato_id}_finalizacao_livro",
                content=response_ato_finalizacao.texto_finalizacao,
                output="binary",
            )
        )

        # Realiza o merge
        response_ato.texto = DOCXMergeModeloMinutaService().execute(
            modelo_content=response_ato.texto,
            minuta_content=finalizacao_docx,
            output="binary"
        )

        # Busca os textos da assinatura
        response_ato_assinatura = TAtoGetTextoAssinaturaAction().execute(t_ato_texto_assinatura_schema)

        if not response_ato_assinatura:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nao encontramos o texto de assinatura para este ato.",
            )

        # Monta o docx das assinaturas
        assinatura_docx = DOCXProcess().execute(
            DOCXProcessSchema(
                id=f"{response_ato.ato_id}_assinatura_livro",
                content=response_ato_assinatura.texto_assinatura if response_ato_assinatura else None,
                output="binary",
            )
        )

        # Realiza o merge
        response_ato.texto = DOCXMergeModeloMinutaService().execute(
            modelo_content=response_ato.texto,
            minuta_content=assinatura_docx,
            output="binary"
        )

        # Salva o DOCX final em disco sem requalificar o conteúdo
        response_ato.texto = DOCXProcess().execute(
            DOCXProcessSchema(
                id=f"{response_ato.ato_id}_display_texto",
                content=response_ato.texto,
                save_disk=True,
                output="path",
            )
        )

        return response_ato
