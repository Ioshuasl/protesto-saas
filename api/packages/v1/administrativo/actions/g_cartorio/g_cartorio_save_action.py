from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_cartorio.g_cartorio_save_repository import (
    GCartorioSaveRepository,
)
from packages.v1.administrativo.schemas.g_cartorio_schema import GCartorioSaveSchema


class GCartorioSaveAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de salvamento de um novo registro na tabela G_GRAMATICA.
    """

    def execute(self, g_cartorio_save_schema: GCartorioSaveSchema):
        """
        Executa a operação de salvamento.

        Args:
            g_cartorio_schema (GCartorioSchema):
                O esquema com os dados a serem persistidos.

        Returns:
            O resultado da operação de salvamento.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        g_cartorio_save_repository = GCartorioSaveRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = g_cartorio_save_repository.execute(g_cartorio_save_schema)

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return response
