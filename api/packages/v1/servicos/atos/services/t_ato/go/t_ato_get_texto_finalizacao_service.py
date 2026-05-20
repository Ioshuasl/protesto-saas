from packages.v1.administrativo.actions.g_marcacao_tipo.g_marcacao_tipo_show_action import GMarcacaoTipoShowAction
from packages.v1.administrativo.controllers.g_marcacao_tipo_controller import GMarcacaoTipoShowService
from packages.v1.administrativo.controllers.t_livro_natureza_controller import TLivroNaturezaShowService
from packages.v1.administrativo.schemas.g_marcacao_tipo_schema import GMarcacaoTipoIdSchema
from packages.v1.administrativo.schemas.t_livro_natureza_schema import TLivroNaturezaIdSchema
from packages.v1.resolver.schemas.resolver_schema import ResolverSchema
from packages.v1.resolver.services.resolver_main_service import ResolverMainService
from packages.v1.servicos.atos.actions.t_ato.t_ato_get_texto_finalizacao_action import TAtoGetTextoFinalizacaoAction
from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoIdSchema, TAtoTextoFinalizacao
from fastapi import HTTPException, status

from packages.v1.servicos.atos.schemas.t_ato_tipo_schema import TAtoTipoIdSchema
from packages.v1.servicos.atos.services.t_ato.go.t_ato_show_service import TAtoShowService
from packages.v1.servicos.atos.services.t_ato_tipo.go.t_ato_tipo_show_service import TAtoTipoShowService


class TAtoGetTextoFinalizacaoService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela T_ATO.
    """

    def execute(self, data: TAtoTextoFinalizacao):

        """
        Executa a operação de busca no banco de dados.
        Args:
            data (TAtoIdSchema):
                O esquema com o ID do registro a ser buscado.

        Returns:
            O resultado da busca.
        """

        if data.tipo_finalizacao == 1:

            data.coluna = 'texto_finalizacao'

        if data.tipo_finalizacao == 2:

            data.coluna = 'texto_finalizacao_traslado'

        response_finalizacao = TAtoGetTextoFinalizacaoAction().execute(data)

        if not response_finalizacao:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nao encontramos o ato informado. Verifique o codigo e tente novamente.",
            )

        if not response_finalizacao.texto_finalizacao:

            response_ato = TAtoShowService().execute(
                TAtoIdSchema(
                    ato_id=response_finalizacao.ato_id
                )
            )

            response_ato_tipo = TAtoTipoShowService().execute(
                TAtoTipoIdSchema(
                    ato_tipo_id=response_ato.ato_tipo_id
                )
            )

            response_livro_natureza = TLivroNaturezaShowService().execute(
                TLivroNaturezaIdSchema(livro_natureza_id=response_ato_tipo.livro_natureza_id)
            )

            if data.tipo_finalizacao == 1:

                tipo_finalizacao = response_livro_natureza.tipo_finalizacao_livro

            if data.tipo_finalizacao == 2:

                tipo_finalizacao = response_livro_natureza.tipo_finalizacao_traslado

            response_marcacao_tipo = GMarcacaoTipoShowAction().execute(
                GMarcacaoTipoIdSchema(
                    marcacao_tipo_id=tipo_finalizacao
                )
            )

            response_finalizacao.texto_finalizacao = response_marcacao_tipo.texto

        response_finalizacao.texto_finalizacao = ResolverMainService().execute(
            ResolverSchema(
                id=response_finalizacao.ato_id,
                campo_id_valor=response_finalizacao.ato_id,
                sitema_id=2,
                texto=response_finalizacao.texto_finalizacao,
            )
        )

        return response_finalizacao
