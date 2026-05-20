from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_natureza_titulo.g_natureza_titulo_save_repository import (
    GNaturezaTituloSaveRepository,
)
from packages.v1.administrativo.schemas.g_natureza_titulo_schema import (
    GNaturezaTituloSaveSchema,
)


class GNaturezaTituloSaveAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de salvamento de um novo registro na tabela G_NATUREZA_TITULO.
    """

    def execute(self, g_natureza_titulo_save_schema: GNaturezaTituloSaveSchema):
        """
        Executa a operação de salvamento.

        Args:
            g_natureza_titulo_schema (GNaturezaTituloSchema):
                O esquema com os dados a serem persistidos.

        Returns:
            O resultado da operação de salvamento.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        g_natureza_titulo_save_repository = GNaturezaTituloSaveRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = g_natureza_titulo_save_repository.execute(
            g_natureza_titulo_save_schema
        )

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return response
