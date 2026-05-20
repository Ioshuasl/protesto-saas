from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_selo_grupo.g_selo_grupo_show_repository import (
    GSeloGrupoShowRepository,
)
from packages.v1.administrativo.schemas.g_selo_grupo_schema import GSeloGrupoIdSchema


class GSeloGrupoShowAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a exibição
    de um registro na tabela G_NATUREZA_TITULO.
    """

    def execute(self, g_selo_grupo_id_schema: GSeloGrupoIdSchema):
        """
        Executa a operação de exibição.

        Args:
            g_selo_grupo_id_schema (GSeloGrupoIdSchema):
                O esquema com o ID do registro a ser exibido.

        Returns:
            O resultado da operação de exibição.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        g_selo_grupo_show_repository = GSeloGrupoShowRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = g_selo_grupo_show_repository.execute(g_selo_grupo_id_schema)

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return response
