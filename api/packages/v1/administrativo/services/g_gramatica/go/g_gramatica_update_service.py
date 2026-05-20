from packages.v1.administrativo.actions.g_gramatica.g_gramatica_update_action import (
    GGramaticaUpdateAction,
)
from packages.v1.administrativo.schemas.g_gramatica_schema import GGramaticaUpdateSchema


class GGramaticaUpdateService:
    """
    Serviço responsável pela operação de atualização de um registro
    na tabela G_GRAMATICA.
    """

    def execute(self, g_gramatica_update_schema: GGramaticaUpdateSchema):
        """
        Executa a operação de atualização no banco de dados.

        Args:
            g_gramatica_update_schema (GGramaticaUpdateSchema):
                O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        g_gramatica_update_action = GGramaticaUpdateAction()

        # ----------------------------------------------------
        # Execução da ação e retorno do resultado
        # ----------------------------------------------------
        return g_gramatica_update_action.execute(g_gramatica_update_schema)
