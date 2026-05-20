from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_emolumento.g_emolumento_show_repository import (
    GEmolumentoShowRepository,
)
from packages.v1.administrativo.schemas.g_emolumento_schema import GEmolumentoIdSchema


class GEmolumentoShowAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a exibição
    de um registro na tabela G_NATUREZA_TITULO.
    """

    def execute(self, g_emolumento_id_schema: GEmolumentoIdSchema):
        """
        Executa a operação de exibição.

        Args:
            g_emolumento_id_schema (GEmolumentoIdSchema):
                O esquema com o ID do registro a ser exibido.

        Returns:
            O resultado da operação de exibição.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        g_emolumento_show_repository = GEmolumentoShowRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = g_emolumento_show_repository.execute(g_emolumento_id_schema)

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return response
