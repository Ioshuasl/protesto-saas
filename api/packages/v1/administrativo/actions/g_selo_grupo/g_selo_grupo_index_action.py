from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_selo_grupo.g_selo_grupo_index_repository import (
    GSeloGrupoIndexRepository,
)


class GSeloGrupoIndexAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de todos os registros na tabela G_NATUREZA_TITULO.
    """

    def execute(self):
        """
        Executa a operação de listagem no banco de dados.

        Args:
            g_selo_grupo_index_schema (GSeloGrupoIndexSchema):
                Esquema contendo parâmetros opcionais de filtro.

        Returns:
            A lista de registros encontrados.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        g_selo_grupo_index_repository = GSeloGrupoIndexRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = g_selo_grupo_index_repository.execute()

        # ----------------------------------------------------
        # Retorno da informação
        # --------------------------------
        return response
