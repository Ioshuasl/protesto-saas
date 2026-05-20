from packages.v1.administrativo.actions.g_gramatica.g_gramatica_show_action import (
    GGramaticaShowAction,
)
from packages.v1.administrativo.schemas.g_gramatica_schema import GGramaticaIdSchema
from fastapi import HTTPException, status


class GGramaticaShowService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela G_GRAMATICA.
    """

    def execute(self, g_gramatica_id_schema: GGramaticaIdSchema):
        """
        Executa a operação de busca no banco de dados.

        Args:
            g_gramatica_id_schema (GGramaticaIdSchema):
                O esquema com o ID do registro a ser buscado.

        Returns:
            O resultado da busca.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        g_gramatica_show_action = GGramaticaShowAction()

        # ----------------------------------------------------
        # Execução da ação
        # ----------------------------------------------------
        data = g_gramatica_show_action.execute(g_gramatica_id_schema)

        # ----------------------------------------------------
        # Verificação de resultado
        # ----------------------------------------------------
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar o registro de G_GRAMATICA.",
            )

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return data
