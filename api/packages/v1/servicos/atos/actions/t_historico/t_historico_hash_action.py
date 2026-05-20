from abstracts.action import BaseAction
from packages.v1.servicos.atos.repositories.t_historico.t_historico_hash_repository import (
    THistoricoHashRepository,
)
from packages.v1.servicos.atos.schemas.t_historico_schema import THistoricoHashSchema


class THistoricoHashAction(BaseAction):
    def execute(self, data: THistoricoHashSchema):
        return THistoricoHashRepository().execute(data)
