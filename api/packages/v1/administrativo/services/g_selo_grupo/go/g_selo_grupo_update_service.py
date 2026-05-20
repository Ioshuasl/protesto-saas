from packages.v1.administrativo.actions.g_selo_grupo.g_selo_grupo_update_action import (
    GSeloGrupoUpdateAction,
)
from packages.v1.administrativo.schemas.g_selo_grupo_schema import (
    GSeloGrupoUpdateSchema,
)


class GSeloGrupoUpdateService:
    """
    Serviço responsável pela operação de atualização de um registro
    na tabela G_SELO_GRUPO.
    """

    def execute(self, g_selo_grupo_update_schema: GSeloGrupoUpdateSchema):
        """
        Executa a operação de atualização no banco de dados.

        Args:
            g_selo_grupo_update_schema (GSeloGrupoUpdateSchema):
                O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        g_selo_grupo_update_action = GSeloGrupoUpdateAction()

        # ----------------------------------------------------
        # Execução da ação e retorno do resultado
        # ----------------------------------------------------
        return g_selo_grupo_update_action.execute(g_selo_grupo_update_schema)
