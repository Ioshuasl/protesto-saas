from packages.v1.administrativo.actions.g_emolumento_item.g_emolumento_item_update_action import (
    GEmolumentoItemUpdateAction,
)
from packages.v1.administrativo.schemas.g_emolumento_item_schema import (
    GEmolumentoItemUpdateSchema,
)


class GEmolumentoItemUpdateService:
    """
    Serviço responsável pela operação de atualização de um registro
    na tabela G_EMOLUMENTO_ITEM.
    """

    def execute(self, g_emolumento_item_update_schema: GEmolumentoItemUpdateSchema):
        """
        Executa a operação de atualização no banco de dados.

        Args:
            g_emolumento_item_update_schema (GEmolumentoItemUpdateSchema):
                O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        g_emolumento_item_update_action = GEmolumentoItemUpdateAction()

        # ----------------------------------------------------
        # Execução da ação e retorno do resultado
        # ----------------------------------------------------
        return g_emolumento_item_update_action.execute(g_emolumento_item_update_schema)
