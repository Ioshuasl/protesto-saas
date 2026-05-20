from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_emolumento_item.g_emolumento_item_save_repository import GEmolumentoItemSaveRepository
from packages.v1.administrativo.schemas.g_emolumento_item_schema import GEmolumentoItemSaveSchema


class GEmolumentoItemSaveAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de salvamento de um novo registro na tabela G_EMOLUMENTO_ITEM.
    """

    def execute(self, g_emolumento_item_save_schema: GEmolumentoItemSaveSchema):
        """
        Executa a operação de salvamento.

        Args:
            g_emolumento_item_schema (GEmolumentoItemSchema):
                O esquema com os dados a serem persistidos.

        Returns:
            O resultado da operação de salvamento.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        g_emolumento_item_save_repository = GEmolumentoItemSaveRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = g_emolumento_item_save_repository.execute(g_emolumento_item_save_schema)

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return response
