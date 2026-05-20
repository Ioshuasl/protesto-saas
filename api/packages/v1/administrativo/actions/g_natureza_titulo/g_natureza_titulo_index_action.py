from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_natureza_titulo.g_natureza_titulo_index_repository import (
    GNaturezaTituloIndexRepository,
)
from packages.v1.administrativo.schemas.g_natureza_titulo_schema import (
    GNaturezaTituloIndexSchema,
)


class GNaturezaTituloIndexAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de todos os registros na tabela G_NATUREZA_TITULO.
    """

    def execute(self, g_natureza_titulo_index_schema: GNaturezaTituloIndexSchema):
        """
        Executa a operação de listagem no banco de dados.

        Args:
            g_natureza_titulo_index_schema (GNaturezaTituloIndexSchema):
                Esquema contendo parâmetros opcionais de filtro.

        Returns:
            A lista de registros encontrados.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        g_natureza_titulo_index_repository = GNaturezaTituloIndexRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = g_natureza_titulo_index_repository.execute(
            g_natureza_titulo_index_schema
        )

        # ----------------------------------------------------
        # Retorno da informação
        # --------------------------------
        return response
