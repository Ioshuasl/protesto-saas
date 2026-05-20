from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_emolumento.g_emolumento_save_repository import (
    GEmolumentoSaveRepository,
)
from packages.v1.administrativo.schemas.g_emolumento_schema import GEmolumentoSaveSchema


class GEmolumentoSaveAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de salvamento de um novo registro na tabela G_EMOLUMENTO.
    """

    def execute(self, g_emolumento_save_schema: GEmolumentoSaveSchema):
        """
        Executa a operação de salvamento.

        Args:
            g_emolumento_schema (GEmolumentoSchema):
                O esquema com os dados a serem persistidos.

        Returns:
            O resultado da operação de salvamento.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        g_emolumento_save_repository = GEmolumentoSaveRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = g_emolumento_save_repository.execute(g_emolumento_save_schema)

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return response
