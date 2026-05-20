from packages.v1.administrativo.actions.g_emolumento_item.g_emolumento_item_index_action import (
    GEmolumentoItemIndexAction,
)
from fastapi import HTTPException, status

from packages.v1.administrativo.schemas.g_emolumento_item_schema import (
    GEmolumentoItemIndexSchema,
)


class GEmolumentoItemIndexService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de registros na tabela G_EMOLUMENTO_ITEM.
    """

    def execute(
        self, g_emolumento_item_emolumento_index_schema: GEmolumentoItemIndexSchema
    ):
        """
        Executa a operação de busca de todos os registros no banco de dados.

        Args:
            g_emolumento_item_index_schema (GEmolumentoItemIndexSchema):
                Esquema que pode conter filtros ou parâmetros de busca.

        Returns:
            A lista de registros encontrados.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        g_emolumento_item_index_action = GEmolumentoItemIndexAction()

        # ----------------------------------------------------
        # Execução da ação
        # ----------------------------------------------------
        data = g_emolumento_item_index_action.execute(
            g_emolumento_item_emolumento_index_schema
        )

        # ----------------------------------------------------
        # Verificação de retorno
        # ----------------------------------------------------
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar registros de G_EMOLUMENTO_ITEM.",
            )

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return data
