from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_emolumento_periodo.g_emolumento_periodo_show_repository import (
    GEmolumentoPeriodoShowRepository,
)
from packages.v1.administrativo.schemas.g_emolumento_periodo_schema import (
    GEmolumentoPeriodoIdSchema,
)


class GEmolumentoPeriodoShowAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a exibição
    de um registro na tabela G_NATUREZA_TITULO.
    """

    def execute(self, g_emolumento_periodo_id_schema: GEmolumentoPeriodoIdSchema):
        """
        Executa a operação de exibição.

        Args:
            g_emolumento_periodo_id_schema (GEmolumentoPeriodoIdSchema):
                O esquema com o ID do registro a ser exibido.

        Returns:
            O resultado da operação de exibição.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        g_emolumento_periodo_show_repository = GEmolumentoPeriodoShowRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = g_emolumento_periodo_show_repository.execute(
            g_emolumento_periodo_id_schema
        )

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return response
