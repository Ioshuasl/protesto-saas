from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_cartorio.g_cartorio_show_repository import (
    GCartorioShowRepository,
)
from packages.v1.administrativo.schemas.g_cartorio_schema import GCartorioIdSchema


class GCartorioShowAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a exibição
    de um registro na tabela G_NATUREZA_TITULO.
    """

    def execute(self, g_cartorio_id_schema: GCartorioIdSchema):
        """
        Executa a operação de exibição.

        Args:
            g_cartorio_id_schema (GCartorioIdSchema):
                O esquema com o ID do registro a ser exibido.

        Returns:
            O resultado da operação de exibição.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        g_cartorio_show_repository = GCartorioShowRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = g_cartorio_show_repository.execute(g_cartorio_id_schema)

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return response
