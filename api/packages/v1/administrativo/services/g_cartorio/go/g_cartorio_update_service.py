from packages.v1.administrativo.actions.g_cartorio.g_cartorio_update_action import (
    GCartorioUpdateAction,
)
from packages.v1.administrativo.schemas.g_cartorio_schema import GCartorioUpdateSchema


class GCartorioUpdateService:
    """
    Serviço responsável pela operação de atualização de um registro
    na tabela G_GRAMATICA.
    """

    def execute(self, g_cartorio_update_schema: GCartorioUpdateSchema):
        """
        Executa a operação de atualização no banco de dados.

        Args:
            g_cartorio_update_schema (GCartorioUpdateSchema):
                O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        g_cartorio_update_action = GCartorioUpdateAction()

        # ----------------------------------------------------
        # Execução da ação e retorno do resultado
        # ----------------------------------------------------
        return g_cartorio_update_action.execute(g_cartorio_update_schema)
