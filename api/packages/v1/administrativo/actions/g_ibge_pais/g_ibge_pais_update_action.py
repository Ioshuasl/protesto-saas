from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_ibge_pais.g_ibge_pais_update_repository import (
    GIbgePaisUpdateRepository,
)
from packages.v1.administrativo.schemas.g_ibge_pais_schema import (
    GIbgePaisUpdateSchema,
)


class GIbgePaisUpdateAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a atualização
    de um registro na tabela {{ entity_upper }}.
    """

    def execute(self, g_ibge_pais_update_schema: GIbgePaisUpdateSchema):
        """
        Executa a operação de atualização.

        Args:
            g_ibge_pais_update_schema (GIbgePaisUpdateSchema):
                O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório de atualização
        # ----------------------------------------------------
        g_ibge_pais_update_repository = GIbgePaisUpdateRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = g_ibge_pais_update_repository.execute(g_ibge_pais_update_schema)

        # ----------------------------------------------------
        # Retorno do resultado
        # ----------------------------------------------------
        return response
