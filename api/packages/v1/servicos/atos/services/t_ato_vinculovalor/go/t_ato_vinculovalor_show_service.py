from packages.v1.servicos.atos.actions.t_ato_vinculovalor.t_ato_vinculovalor_show_action import (
    TAtoVinculoValorShowAction,
)
from packages.v1.servicos.atos.schemas.t_ato_vinculovalor_schema import (
    TAtoVinculoValorIdSchema,
)
from fastapi import HTTPException, status


class TAtoVinculoValorShowService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela T_ATO_VINCULOVALOR.
    """

    def execute(self, t_ato_vinculovalor_id_schema: TAtoVinculoValorIdSchema):
        """
        Executa a operação de busca no banco de dados.

        Args:
            t_ato_vinculovalor_id_schema (TAtoVinculoValorIdSchema):
                O esquema com o ID do registro a ser buscado.

        Returns:
            O resultado da busca.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        t_ato_vinculovalor_show_action = TAtoVinculoValorShowAction()

        # ----------------------------------------------------
        # Execução da ação
        # ----------------------------------------------------
        data = t_ato_vinculovalor_show_action.execute(t_ato_vinculovalor_id_schema)

        # ----------------------------------------------------
        # Verificação de resultado
        # ----------------------------------------------------
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar o registro de T_ATO_VINCULOVALOR.",
            )

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return data
