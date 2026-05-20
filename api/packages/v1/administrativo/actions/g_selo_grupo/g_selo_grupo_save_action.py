from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_selo_grupo.g_selo_grupo_save_repository import (
    GSeloGrupoSaveRepository,
)
from packages.v1.administrativo.schemas.g_selo_grupo_schema import GSeloGrupoSaveSchema


class GSeloGrupoSaveAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de salvamento de um novo registro na tabela G_GRAMATICA.
    """

    def execute(self, g_selo_grupo_save_schema: GSeloGrupoSaveSchema):
        """
        Executa a operação de salvamento.

        Args:
            g_selo_grupo_schema (GSeloGrupoSchema):
                O esquema com os dados a serem persistidos.

        Returns:
            O resultado da operação de salvamento.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        g_selo_grupo_save_repository = GSeloGrupoSaveRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = g_selo_grupo_save_repository.execute(g_selo_grupo_save_schema)

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return response
