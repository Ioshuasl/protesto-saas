from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_ibge_pais.g_ibge_pais_save_repository import (
    GIbgePaisSaveRepository,
)
from packages.v1.administrativo.schemas.g_ibge_pais_schema import (
    GIbgePaisSaveSchema,
)


class GIbgePaisSaveAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de salvamento de um novo registro na tabela {{ entity_upper }}.
    """

    def execute(self, g_ibge_pais_save_schema: GIbgePaisSaveSchema):
        """
        Executa a operação de salvamento.

        Args:
            g_ibge_pais_save_schema (GIbgePaisSaveSchema):
                O esquema com os dados a serem persistidos.

        Returns:
            O resultado da operação de salvamento.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        g_ibge_pais_save_repository = GIbgePaisSaveRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = g_ibge_pais_save_repository.execute(g_ibge_pais_save_schema)

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return response
