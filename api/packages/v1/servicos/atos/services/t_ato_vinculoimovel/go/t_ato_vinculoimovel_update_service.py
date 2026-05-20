from packages.v1.servicos.atos.actions.t_ato_vinculoimovel.t_ato_vinculoimovel_update_action import (
    TAtoVinculoImovelUpdateAction,
)
from packages.v1.servicos.atos.schemas.t_ato_vinculoimovel_schema import (
    TAtoVinculoImovelUpdateSchema,
)


class TAtoVinculoImovelUpdateService:
    """
    Serviço responsável pela operação de atualização de um registro
    na tabela T_ATO_VINCULOIMOVEL.
    """

    def execute(self, t_ato_vinculoimovel_update_schema: TAtoVinculoImovelUpdateSchema):
        """
        Executa a operação de atualização no banco de dados.

        Args:
            t_ato_vinculoimovel_update_schema (TAtoVinculoImovelUpdateSchema):
                O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        t_ato_vinculoimovel_update_action = TAtoVinculoImovelUpdateAction()

        # ----------------------------------------------------
        # Execução da ação e retorno do resultado
        # ----------------------------------------------------
        return t_ato_vinculoimovel_update_action.execute(
            t_ato_vinculoimovel_update_schema
        )
