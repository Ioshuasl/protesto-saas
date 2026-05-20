from abstracts.action import BaseAction
from packages.v1.servicos.atos.repositories.t_historico.t_historico_update_repository import (
    THistoricoUpdateRepository,
)
from packages.v1.servicos.atos.schemas.t_historico_schema import (
    THistoricoUpdateSchema,
)


class THistoricoUpdateAction(BaseAction):
    """
    Action responsável por encapsular a lógica de negócio para a operação
    de atualização de um registro em T_HISTORICO
    """

    def execute(self, schema: THistoricoUpdateSchema):
        repository = THistoricoUpdateRepository()
        return repository.execute(schema)
