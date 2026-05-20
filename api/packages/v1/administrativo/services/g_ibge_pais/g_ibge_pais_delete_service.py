from packages.v1.administrativo.actions.g_ibge_pais.g_ibge_pais_delete_action import (
    GIbgePaisDeleteAction,
)
from packages.v1.administrativo.schemas.g_ibge_pais_schema import (
    GIbgePaisIdSchema,
)


class GIbgePaisDeleteService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de exclusão de um registro na tabela {{ entity_upper }}.
    """

    def execute(self, g_ibge_pais_id_schema: GIbgePaisIdSchema):
        """
        Executa a operação de exclusão do registro no banco de dados.

        Args:
            g_ibge_pais_id_schema (GIbgePaisIdSchema):
                O esquema com o ID do registro a ser excluído.

        Returns:
            O resultado da operação de exclusão.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        g_ibge_pais_delete_action = GIbgePaisDeleteAction()

        # ----------------------------------------------------
        # Execução da ação
        # ----------------------------------------------------
        data = g_ibge_pais_delete_action.execute(g_ibge_pais_id_schema)

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return data
