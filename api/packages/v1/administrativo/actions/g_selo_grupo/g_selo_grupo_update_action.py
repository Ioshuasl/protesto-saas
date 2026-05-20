from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_selo_grupo.g_selo_grupo_update_repository import (
    GSeloGrupoUpdateRepository,
)
from packages.v1.administrativo.schemas.g_selo_grupo_schema import (
    GSeloGrupoUpdateSchema,
)


class GSeloGrupoUpdateAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a atualização
    de um registro na tabela G_NATUREZA_TITULO.
    """

    def execute(self, g_selo_grupo_update_schema: GSeloGrupoUpdateSchema):
        """
        Executa a operação de atualização.

        Args:
            g_selo_grupo_update_schema (GSeloGrupoUpdateSchema):
                O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório de atualização
        # ----------------------------------------------------
        g_selo_grupo_update_repository = GSeloGrupoUpdateRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = g_selo_grupo_update_repository.execute(g_selo_grupo_update_schema)

        # ----------------------------------------------------
        # Retorno do resultado
        # ----------------------------------------------------
        return response
