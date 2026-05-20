from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_gramatica.g_gramatica_index_repository import (
    GGramaticaIndexRepository,
)


class GGramaticaIndexAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de todos os registros na tabela G_NATUREZA_TITULO.
    """

    def execute(self):
        """
        Executa a operação de listagem no banco de dados.

        Args:
            g_gramatica_index_schema (GGramaticaIndexSchema):
                Esquema contendo parâmetros opcionais de filtro.

        Returns:
            A lista de registros encontrados.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        g_gramatica_index_repository = GGramaticaIndexRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = g_gramatica_index_repository.execute()

        # ----------------------------------------------------
        # Retorno da informação
        # --------------------------------
        return response
