from abstracts.action import BaseAction
from packages.v1.servicos.atos.repositories.t_historico.t_historico_delete_repository import (
    THistoricoDeleteRepository,
)
from packages.v1.servicos.atos.schemas.t_historico_schema import (
    THistoricoIdSchema,
)


class THistoricoDeleteAction(BaseAction):
    """
    Action responsável por encapsular a lógica de negócio para a operação
    de exclusão de um registro em T_HISTORICO
    """

    def execute(self, schema: THistoricoIdSchema):
        repository = THistoricoDeleteRepository()
        return repository.execute(schema)
