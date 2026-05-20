from packages.v1.servicos.atos.actions.t_historico.t_historico_index_action import (
    THistoricoIndexAction,
)
from packages.v1.servicos.atos.schemas.t_historico_schema import THistoricoIndexSchema


class THistoricoIndexService:
    """
    Serviço responsável por encapsular a lógica de negócio
    para listagem de registros de T_HISTORICO
    """

    def execute(self, data: THistoricoIndexSchema):
        action = THistoricoIndexAction()
        return action.execute(data)
