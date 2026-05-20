from packages.v1.administrativo.actions.g_cartorio.g_cartorio_show_action import (
    GCartorioShowAction,
)
from packages.v1.administrativo.schemas.g_cartorio_schema import GCartorioIdSchema
from fastapi import HTTPException, status


class GCartorioShowService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela G_GRAMATICA.
    """

    def execute(self, g_cartorio_id_schema: GCartorioIdSchema):
        """
        Executa a operação de busca no banco de dados.

        Args:
            g_cartorio_id_schema (GCartorioIdSchema):
                O esquema com o ID do registro a ser buscado.

        Returns:
            O resultado da busca.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        g_cartorio_show_action = GCartorioShowAction()

        # ----------------------------------------------------
        # Execução da ação
        # ----------------------------------------------------
        data = g_cartorio_show_action.execute(g_cartorio_id_schema)

        # ----------------------------------------------------
        # Verificação de resultado
        # ----------------------------------------------------
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar o registro de G_GRAMATICA.",
            )

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return data
