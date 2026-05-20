from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_ibge_pais.g_ibge_pais_index_repository import (
    GIbgePaisIndexRepository,
)


class GIbgePaisIndexAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de todos os registros na tabela {{ entity_upper }}.
    """

    def execute(self):
        """
        Executa a operação de listagem no banco de dados.

        Args:
            g_ibge_pais_index_schema (GIbgePaisIndexSchema):
                Esquema contendo parâmetros opcionais de filtro.

        Returns:
            A lista de registros encontrados.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        g_ibge_pais_index_repository = GIbgePaisIndexRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = g_ibge_pais_index_repository.execute()

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return response
