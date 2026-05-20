from packages.v1.administrativo.actions.g_emolumento.g_emolumento_update_action import (
    GEmolumentoUpdateAction,
)
from packages.v1.administrativo.schemas.g_emolumento_schema import (
    GEmolumentoUpdateSchema,
)


class GEmolumentoUpdateService:
    """
    Serviço responsável pela operação de atualização de um registro
    na tabela G_EMOLUMENTO.
    """

    def execute(self, g_emolumento_update_schema: GEmolumentoUpdateSchema):
        """
        Executa a operação de atualização no banco de dados.

        Args:
            g_emolumento_update_schema (GEmolumentoUpdateSchema):
                O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        g_emolumento_update_action = GEmolumentoUpdateAction()

        # ----------------------------------------------------
        # Execução da ação e retorno do resultado
        # ----------------------------------------------------
        return g_emolumento_update_action.execute(g_emolumento_update_schema)
