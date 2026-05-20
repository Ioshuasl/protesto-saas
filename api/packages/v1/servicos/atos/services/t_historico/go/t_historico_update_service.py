from packages.v1.servicos.atos.actions.t_historico.t_historico_update_action import (
    THistoricoUpdateAction,
)
from packages.v1.servicos.atos.schemas.t_historico_schema import (
    THistoricoUpdateSchema,
)


class THistoricoUpdateService:
    """
    Serviço responsável por encapsular a lógica de negócio
    para atualização de um registro em T_HISTORICO
    """

    def execute(self, schema: THistoricoUpdateSchema):
        action = THistoricoUpdateAction()
        return action.execute(schema)
