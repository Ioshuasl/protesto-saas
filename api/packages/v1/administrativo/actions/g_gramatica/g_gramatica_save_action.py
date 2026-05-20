from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_gramatica.g_gramatica_save_repository import (
    GGramaticaSaveRepository,
)
from packages.v1.administrativo.schemas.g_gramatica_schema import GGramaticaSaveSchema


class GGramaticaSaveAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de salvamento de um novo registro na tabela G_GRAMATICA.
    """

    def execute(self, g_gramatica_save_schema: GGramaticaSaveSchema):
        """
        Executa a operação de salvamento.

        Args:
            g_gramatica_schema (GGramaticaSchema):
                O esquema com os dados a serem persistidos.

        Returns:
            O resultado da operação de salvamento.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        g_gramatica_save_repository = GGramaticaSaveRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = g_gramatica_save_repository.execute(g_gramatica_save_schema)

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return response
