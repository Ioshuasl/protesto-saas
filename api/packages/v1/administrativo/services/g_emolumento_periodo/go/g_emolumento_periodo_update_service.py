from packages.v1.administrativo.actions.g_emolumento_periodo.g_emolumento_periodo_update_action import (
    GEmolumentoPeriodoUpdateAction,
)
from packages.v1.administrativo.schemas.g_emolumento_periodo_schema import (
    GEmolumentoPeriodoUpdateSchema,
)


class GEmolumentoPeriodoUpdateService:
    """
    Serviço responsável pela operação de atualização de um registro
    na tabela G_EMOLUMENTO_PERIODO.
    """

    def execute(
        self, g_emolumento_periodo_update_schema: GEmolumentoPeriodoUpdateSchema
    ):
        """
        Executa a operação de atualização no banco de dados.

        Args:
            g_emolumento_periodo_update_schema (GEmolumentoPeriodoUpdateSchema):
                O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        g_emolumento_periodo_update_action = GEmolumentoPeriodoUpdateAction()

        # ----------------------------------------------------
        # Execução da ação e retorno do resultado
        # ----------------------------------------------------
        return g_emolumento_periodo_update_action.execute(
            g_emolumento_periodo_update_schema
        )
