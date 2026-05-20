from packages.v1.administrativo.actions.g_natureza_titulo.g_natureza_titulo_update_action import (
    GNaturezaTituloUpdateAction,
)
from packages.v1.administrativo.schemas.g_natureza_titulo_schema import (
    GNaturezaTituloUpdateSchema,
)


class GNaturezaTituloUpdateService:
    """
    Serviço responsável pela operação de atualização de um registro
    na tabela G_NATUREZA_TITULO.
    """

    def execute(self, g_natureza_titulo_update_schema: GNaturezaTituloUpdateSchema):
        """
        Executa a operação de atualização no banco de dados.

        Args:
            g_natureza_titulo_update_schema (GNaturezaTituloUpdateSchema):
                O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        g_natureza_titulo_update_action = GNaturezaTituloUpdateAction()

        # ----------------------------------------------------
        # Execução da ação e retorno do resultado
        # ----------------------------------------------------
        return g_natureza_titulo_update_action.execute(g_natureza_titulo_update_schema)
