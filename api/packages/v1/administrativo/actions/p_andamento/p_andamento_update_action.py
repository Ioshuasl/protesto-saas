from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_andamento.p_andamento_update_repository import (
    UpdateRepository,
)
from packages.v1.administrativo.schemas.p_andamento_schema import PAndamentoUpdateSchema


class UpdateAction(BaseAction):
    def execute(self, andamento_id: int, andamento_schema: PAndamentoUpdateSchema):
        return UpdateRepository().execute(andamento_id, andamento_schema)
