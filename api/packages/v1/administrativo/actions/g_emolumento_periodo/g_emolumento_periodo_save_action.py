from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_emolumento_periodo.g_emolumento_periodo_save_repository import (
    GEmolumentoPeriodoSaveRepository,
)
from packages.v1.administrativo.schemas.g_emolumento_periodo_schema import (
    GEmolumentoPeriodoSaveSchema,
)


class GEmolumentoPeriodoSaveAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de salvamento de um novo registro na tabela G_GRAMATICA.
    """

    def execute(self, g_emolumento_periodo_save_schema: GEmolumentoPeriodoSaveSchema):
        """
        Executa a operação de salvamento.

        Args:
            g_emolumento_periodo_schema (GEmolumentoPeriodoSchema):
                O esquema com os dados a serem persistidos.

        Returns:
            O resultado da operação de salvamento.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        g_emolumento_periodo_save_repository = GEmolumentoPeriodoSaveRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = g_emolumento_periodo_save_repository.execute(
            g_emolumento_periodo_save_schema
        )

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return response
