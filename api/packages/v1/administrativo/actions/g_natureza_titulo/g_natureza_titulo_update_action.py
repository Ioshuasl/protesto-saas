from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_natureza_titulo.g_natureza_titulo_update_repository import (
    GNaturezaTituloUpdateRepository,
)
from packages.v1.administrativo.schemas.g_natureza_titulo_schema import (
    GNaturezaTituloUpdateSchema,
)


class GNaturezaTituloUpdateAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a atualização
    de um registro na tabela G_NATUREZA_TITULO.
    """

    def execute(self, g_natureza_titulo_update_schema: GNaturezaTituloUpdateSchema):
        """
        Executa a operação de atualização.

        Args:
            g_natureza_titulo_update_schema (GNaturezaTituloUpdateSchema):
                O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório de atualização
        # ----------------------------------------------------
        g_natureza_titulo_update_repository = GNaturezaTituloUpdateRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = g_natureza_titulo_update_repository.execute(
            g_natureza_titulo_update_schema
        )

        # ----------------------------------------------------
        # Retorno do resultado
        # ----------------------------------------------------
        return response
