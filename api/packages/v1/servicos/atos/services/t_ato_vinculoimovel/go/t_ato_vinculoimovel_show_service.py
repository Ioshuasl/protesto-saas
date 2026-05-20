from packages.v1.servicos.atos.actions.t_ato_vinculoimovel.t_ato_vinculoimovel_show_action import (
    TAtoVinculoImovelShowAction,
)
from packages.v1.servicos.atos.schemas.t_ato_vinculoimovel_schema import (
    TAtoVinculoImovelIdSchema,
)
from fastapi import HTTPException, status


class TAtoVinculoImovelShowService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela T_ATO_VINCULOIMOVEL.
    """

    def execute(self, t_ato_vinculoimovel_id_schema: TAtoVinculoImovelIdSchema):
        """
        Executa a operação de busca no banco de dados.

        Args:
            t_ato_vinculoimovel_id_schema (TAtoVinculoImovelIdSchema):
                O esquema com o ID do registro a ser buscado.

        Returns:
            O resultado da busca.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        t_ato_vinculoimovel_show_action = TAtoVinculoImovelShowAction()

        # ----------------------------------------------------
        # Execução da ação
        # ----------------------------------------------------
        data = t_ato_vinculoimovel_show_action.execute(t_ato_vinculoimovel_id_schema)

        # ----------------------------------------------------
        # Verificação de resultado
        # ----------------------------------------------------
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar o registro de T_ATO_VINCULOIMOVEL.",
            )

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return data
