from packages.v1.servicos.atos.actions.t_historico.t_historico_show_action import (
    THistoricoShowAction,
)
from packages.v1.servicos.atos.schemas.t_historico_schema import (
    THistoricoIdSchema,
)


class THistoricoShowService:
    """
    Serviço responsável por encapsular a lógica de negócio
    para busca de um registro específico de .T_HISTORICO
    """

    def execute(self, schema: THistoricoIdSchema):
        action = THistoricoShowAction()
        return action.execute(schema)
