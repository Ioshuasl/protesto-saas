from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_gramatica.g_gramatica_show_repository import (
    GGramaticaShowRepository,
)
from packages.v1.administrativo.schemas.g_gramatica_schema import GGramaticaIdSchema


class GGramaticaShowAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a exibição
    de um registro na tabela G_NATUREZA_TITULO.
    """

    def execute(self, g_gramatica_id_schema: GGramaticaIdSchema):
        """
        Executa a operação de exibição.

        Args:
            g_gramatica_id_schema (GGramaticaIdSchema):
                O esquema com o ID do registro a ser exibido.

        Returns:
            O resultado da operação de exibição.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        g_gramatica_show_repository = GGramaticaShowRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = g_gramatica_show_repository.execute(g_gramatica_id_schema)

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return response
