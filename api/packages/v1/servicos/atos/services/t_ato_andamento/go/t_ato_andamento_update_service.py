from packages.v1.servicos.atos.actions.t_ato_andamento.t_ato_andamento_update_action import (
    TAtoAndamentoUpdateAction,
)
from packages.v1.servicos.atos.schemas.t_ato_andamento_schema import (
    TAtoAndamentoUpdateSchema,
)


class TAtoAndamentoUpdateService:
    """
    Serviço responsável pela operação de atualização de um registro
    na tabela T_ATO_ANDAMENTO.
    """

    def execute(self, t_ato_andamento_update_schema: TAtoAndamentoUpdateSchema):
        """
        Executa a operação de atualização no banco de dados.

        Args:
            t_ato_andamento_update_schema (TAtoAndamentoUpdateSchema):
                O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        t_ato_andamento_update_action = TAtoAndamentoUpdateAction()

        # ----------------------------------------------------
        # Execução da ação e retorno do resultado
        # ----------------------------------------------------
        return t_ato_andamento_update_action.execute(
            t_ato_andamento_update_schema
        )
