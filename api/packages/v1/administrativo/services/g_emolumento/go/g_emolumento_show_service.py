from packages.v1.administrativo.actions.g_emolumento.g_emolumento_show_action import (
    GEmolumentoShowAction,
)
from packages.v1.administrativo.schemas.g_emolumento_schema import (
    GEmolumentoIdSchema,
)
from fastapi import HTTPException, status


class GEmolumentoShowService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela G_EMOLUMENTO.
    """

    def execute(self, g_emolumento_id_schema: GEmolumentoIdSchema):
        """
        Executa a operação de busca no banco de dados.

        Args:
            g_emolumento_id_schema (GEmolumentoIdSchema):
                O esquema com o ID do registro a ser buscado.

        Returns:
            O resultado da busca.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        g_emolumento_show_action = GEmolumentoShowAction()

        # ----------------------------------------------------
        # Execução da ação
        # ----------------------------------------------------
        data = g_emolumento_show_action.execute(g_emolumento_id_schema)

        # ----------------------------------------------------
        # Verificação de resultado
        # ----------------------------------------------------
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar o registro de G_EMOLUMENTO.",
            )

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return data
