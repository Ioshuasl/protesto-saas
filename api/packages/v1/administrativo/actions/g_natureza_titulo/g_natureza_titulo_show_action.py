from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_natureza_titulo.g_natureza_titulo_show_repository import (
    GNaturezaTituloShowRepository,
)
from packages.v1.administrativo.schemas.g_natureza_titulo_schema import (
    GNaturezaTituloIdSchema,
)


class GNaturezaTituloShowAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a exibição
    de um registro na tabela G_NATUREZA_TITULO.
    """

    def execute(self, g_natureza_titulo_id_schema: GNaturezaTituloIdSchema):
        """
        Executa a operação de exibição.

        Args:
            g_natureza_titulo_id_schema (GNaturezaTituloIdSchema):
                O esquema com o ID do registro a ser exibido.

        Returns:
            O resultado da operação de exibição.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        g_natureza_titulo_show_repository = GNaturezaTituloShowRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = g_natureza_titulo_show_repository.execute(
            g_natureza_titulo_id_schema
        )

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return response
