from packages.v1.servicos.atos.actions.t_ato.t_ato_update_action import (
    TAtoUpdateAction,
)
from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoUpdateSchema


class TAtoUpdateService:
    """
    Serviço responsável pela operação de atualização de um registro
    na tabela T_ATO.
    """

    def execute(self, t_ato_update_schema: TAtoUpdateSchema):
        """
        Executa a operação de atualização no banco de dados.

        Args:
            t_ato_update_schema (TAtoUpdateSchema):
                O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        t_ato_update_action = TAtoUpdateAction()

        # ----------------------------------------------------
        # Execução da ação e retorno do resultado
        # ----------------------------------------------------
        return t_ato_update_action.execute(t_ato_update_schema)
