from packages.v1.administrativo.actions.g_emolumento_periodo.g_emolumento_periodo_index_action import (
    GEmolumentoPeriodoIndexAction,
)
from fastapi import HTTPException, status


class GEmolumentoPeriodoIndexService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de registros na tabela G_EMOLUMENTO_PERIODO.
    """

    def execute(self):
        """
        Executa a operação de busca de todos os registros no banco de dados.

        Args:
            g_emolumento_periodo_index_schema (GEmolumentoPeriodoIndexSchema):
                Esquema que pode conter filtros ou parâmetros de busca.

        Returns:
            A lista de registros encontrados.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        g_emolumento_periodo_index_action = GEmolumentoPeriodoIndexAction()

        # ----------------------------------------------------
        # Execução da ação
        # ----------------------------------------------------
        data = g_emolumento_periodo_index_action.execute()

        # ----------------------------------------------------
        # Verificação de retorno
        # ----------------------------------------------------
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar registros de G_EMOLUMENTO_PERIODO.",
            )

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return data
