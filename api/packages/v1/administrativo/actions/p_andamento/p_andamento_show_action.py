from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_andamento.p_andamento_show_repository import (
    ShowRepository,
)
from packages.v1.administrativo.schemas.p_andamento_schema import PAndamentoIdSchema


class ShowAction(BaseAction):
    def execute(self, andamento_schema: PAndamentoIdSchema):
        return ShowRepository().execute(andamento_schema)
