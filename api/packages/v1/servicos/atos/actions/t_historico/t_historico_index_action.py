from abstracts.action import BaseAction
from packages.v1.servicos.atos.repositories.t_historico.t_historico_index_repository import (
    THistoricoIndexRepository,
)
from packages.v1.servicos.atos.schemas.t_historico_schema import THistoricoIndexSchema


class THistoricoIndexAction(BaseAction):
    """
    Action responsável por encapsular a lógica de negócio para a operação
    de listagem de registros de T_HISTORICO
    """

    def execute(self, data: THistoricoIndexSchema):
        repository = THistoricoIndexRepository()
        return repository.execute(data)
