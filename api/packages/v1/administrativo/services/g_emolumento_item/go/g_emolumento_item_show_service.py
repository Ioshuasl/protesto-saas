from packages.v1.administrativo.actions.g_emolumento_item.g_emolumento_item_show_action import (
    GEmolumentoItemShowAction,
)
from packages.v1.administrativo.schemas.g_emolumento_item_schema import (
    GEmolumentoItemIdSchema,
)
from fastapi import HTTPException, status


class GEmolumentoItemShowService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela G_EMOLUMENTO_ITEM.
    """

    def execute(self, g_emolumento_item_id_schema: GEmolumentoItemIdSchema):
        """
        Executa a operação de busca no banco de dados.

        Args:
            g_emolumento_item_id_schema (GEmolumentoItemIdSchema):
                O esquema com o ID do registro a ser buscado.

        Returns:
            O resultado da busca.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        g_emolumento_item_show_action = GEmolumentoItemShowAction()

        # ----------------------------------------------------
        # Execução da ação
        # ----------------------------------------------------
        data = g_emolumento_item_show_action.execute(g_emolumento_item_id_schema)

        # ----------------------------------------------------
        # Verificação de resultado
        # ----------------------------------------------------
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar o registro de G_EMOLUMENTO_ITEM.",
            )

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return data
