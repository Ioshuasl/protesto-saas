from packages.v1.administrativo.actions.g_ibge_pais.g_ibge_pais_update_action import (
    GIbgePaisUpdateAction,
)
from packages.v1.administrativo.schemas.g_ibge_pais_schema import (
    GIbgePaisUpdateSchema,
)


class GIbgePaisUpdateService:
    """
    Serviço responsável pela operação de atualização de um registro
    na tabela {{ entity_upper }}.
    """

    def execute(self, g_ibge_pais_update_schema: GIbgePaisUpdateSchema):
        """
        Executa a operação de atualização no banco de dados.

        Args:
            g_ibge_pais_update_schema (GIbgePaisUpdateSchema):
                O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        g_ibge_pais_update_action = GIbgePaisUpdateAction()

        # ----------------------------------------------------
        # Execução da ação e retorno do resultado
        # ----------------------------------------------------
        return g_ibge_pais_update_action.execute(g_ibge_pais_update_schema)
