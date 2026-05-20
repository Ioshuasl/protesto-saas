from abstracts.action import BaseAction
from packages.v1.servicos.atos.repositories.t_historico.t_historico_show_repository import (
    THistoricoShowRepository,
)
from packages.v1.servicos.atos.schemas.t_historico_schema import (
    THistoricoIdSchema,
)


class THistoricoShowAction(BaseAction):
    """
    Action responsável por encapsular a lógica de negócio para a operação
    de busca de um registro específico de T_HISTORICO
    """

    def execute(self, schema: THistoricoIdSchema):
        repository = THistoricoShowRepository()
        return repository.execute(schema)
