from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_cartorio.g_cartorio_update_repository import (
    GCartorioUpdateRepository,
)
from packages.v1.administrativo.schemas.g_cartorio_schema import GCartorioUpdateSchema


class GCartorioUpdateAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a atualização
    de um registro na tabela G_NATUREZA_TITULO.
    """

    def execute(self, g_cartorio_update_schema: GCartorioUpdateSchema):
        """
        Executa a operação de atualização.

        Args:
            g_cartorio_update_schema (GCartorioUpdateSchema):
                O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório de atualização
        # ----------------------------------------------------
        g_cartorio_update_repository = GCartorioUpdateRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = g_cartorio_update_repository.execute(g_cartorio_update_schema)

        # ----------------------------------------------------
        # Retorno do resultado
        # ----------------------------------------------------
        return response
