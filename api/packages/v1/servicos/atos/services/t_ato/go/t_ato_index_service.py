from packages.v1.servicos.atos.actions.t_ato.t_ato_index_action import (
    TAtoIndexAction,
)
from fastapi import HTTPException, status


class TAtoIndexService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de registros na tabela T_ATO.
    """

    def execute(self):
        """
        Executa a operação de busca de todos os registros no banco de dados.

        Args:
            t_ato_index_schema (TAtoIndexSchema):
                Esquema que pode conter filtros ou parâmetros de busca.

        Returns:
            A lista de registros encontrados.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        t_ato_index_action = TAtoIndexAction()

        # ----------------------------------------------------
        # Execução da ação
        # ----------------------------------------------------
        data = t_ato_index_action.execute()

        # ----------------------------------------------------
        # Verificação de retorno
        # ----------------------------------------------------
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nenhum ato foi encontrado para os filtros informados.",
            )

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return data
