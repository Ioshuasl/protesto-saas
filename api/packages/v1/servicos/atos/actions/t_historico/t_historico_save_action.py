from abstracts.action import BaseAction
from packages.v1.servicos.atos.repositories.t_historico.t_historico_save_repository import (
    THistoricoSaveRepository,
)
from packages.v1.servicos.atos.schemas.t_historico_schema import (
    THistoricoSaveSchema,
)


class THistoricoSaveAction(BaseAction):
    """
    Action responsável por encapsular a lógica de negócio para a operação
    de criação de um registro em T_HISTORICO
    """

    def execute(self, schema: THistoricoSaveSchema):
        repository = THistoricoSaveRepository()
        return repository.execute(schema)
