from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_ibge_pais.g_ibge_pais_show_repository import (
    GIbgePaisShowRepository,
)
from packages.v1.administrativo.schemas.g_ibge_pais_schema import (
    GIbgePaisIdSchema,
)


class GIbgePaisShowAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a exibição
    de um registro na tabela {{ entity_upper }}.
    """

    def execute(self, g_ibge_pais_id_schema: GIbgePaisIdSchema):
        """
        Executa a operação de exibição.

        Args:
            g_ibge_pais_id_schema (GIbgePaisIdSchema):
                O esquema com o ID do registro a ser exibido.

        Returns:
            O resultado da operação de exibição.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        g_ibge_pais_show_repository = GIbgePaisShowRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = g_ibge_pais_show_repository.execute(g_ibge_pais_id_schema)

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return response
