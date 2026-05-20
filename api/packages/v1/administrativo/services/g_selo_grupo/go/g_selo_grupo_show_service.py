from packages.v1.administrativo.actions.g_selo_grupo.g_selo_grupo_show_action import (
    GSeloGrupoShowAction,
)
from packages.v1.administrativo.schemas.g_selo_grupo_schema import GSeloGrupoIdSchema
from fastapi import HTTPException, status


class GSeloGrupoShowService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela G_SELO_GRUPO.
    """

    def execute(self, g_selo_grupo_id_schema: GSeloGrupoIdSchema):
        """
        Executa a operação de busca no banco de dados.

        Args:
            g_selo_grupo_id_schema (GSeloGrupoIdSchema):
                O esquema com o ID do registro a ser buscado.

        Returns:
            O resultado da busca.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        g_selo_grupo_show_action = GSeloGrupoShowAction()

        # ----------------------------------------------------
        # Execução da ação
        # ----------------------------------------------------
        data = g_selo_grupo_show_action.execute(g_selo_grupo_id_schema)

        # ----------------------------------------------------
        # Verificação de resultado
        # ----------------------------------------------------
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar o registro de G_SELO_GRUPO.",
            )

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return data
