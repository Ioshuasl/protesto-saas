from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_ibge_pais.g_ibge_pais_delete_repository import (
    GIbgePaisDeleteRepository,
)
from packages.v1.administrativo.schemas.g_ibge_pais_schema import GIbgePaisIdSchema


class GIbgePaisDeleteAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de exclusão de um registro na tabela {{ entity_upper }}.
    """

    def execute(self, g_ibge_pais_id_schema: GIbgePaisIdSchema):
        """
        Executa a operação de exclusão no banco de dados.

        Args:
            g_ibge_pais_id_schema (GIbgePaisIdSchema):
                O esquema contendo o ID do registro a ser excluído.

        Returns:
            O resultado da operação de exclusão.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        g_ibge_pais_delete_repository = GIbgePaisDeleteRepository()

        # ----------------------------------------------------
        # Execução da exclusão
        # ----------------------------------------------------
        response = g_ibge_pais_delete_repository.execute(g_ibge_pais_id_schema)

        return response
