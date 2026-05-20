from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_gramatica.g_gramatica_update_repository import (
    GGramaticaUpdateRepository,
)
from packages.v1.administrativo.schemas.g_gramatica_schema import GGramaticaUpdateSchema


class GGramaticaUpdateAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a atualização
    de um registro na tabela G_NATUREZA_TITULO.
    """

    def execute(self, g_gramatica_update_schema: GGramaticaUpdateSchema):
        """
        Executa a operação de atualização.

        Args:
            g_gramatica_update_schema (GGramaticaUpdateSchema):
                O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório de atualização
        # ----------------------------------------------------
        g_gramatica_update_repository = GGramaticaUpdateRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = g_gramatica_update_repository.execute(g_gramatica_update_schema)

        # ----------------------------------------------------
        # Retorno do resultado
        # ----------------------------------------------------
        return response
