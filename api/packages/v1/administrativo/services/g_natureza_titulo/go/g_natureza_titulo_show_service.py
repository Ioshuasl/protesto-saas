from packages.v1.administrativo.actions.g_natureza_titulo.g_natureza_titulo_show_action import (
    GNaturezaTituloShowAction,
)
from packages.v1.administrativo.schemas.g_natureza_titulo_schema import (
    GNaturezaTituloIdSchema,
)
from fastapi import HTTPException, status


class GNaturezaTituloShowService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela G_NATUREZA_TITULO.
    """

    def execute(self, g_natureza_titulo_id_schema: GNaturezaTituloIdSchema):
        """
        Executa a operação de busca no banco de dados.

        Args:
            g_natureza_titulo_id_schema (GNaturezaTituloIdSchema):
                O esquema com o ID do registro a ser buscado.

        Returns:
            O resultado da busca.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        g_natureza_titulo_show_action = GNaturezaTituloShowAction()

        # ----------------------------------------------------
        # Execução da ação
        # ----------------------------------------------------
        data = g_natureza_titulo_show_action.execute(g_natureza_titulo_id_schema)

        # ----------------------------------------------------
        # Verificação de resultado
        # ----------------------------------------------------
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar o registro de G_NATUREZA_TITULO.",
            )

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return data
