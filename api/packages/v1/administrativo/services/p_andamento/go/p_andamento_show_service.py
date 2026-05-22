from packages.v1.administrativo.actions.p_andamento.p_andamento_show_action import ShowAction
from packages.v1.administrativo.schemas.p_andamento_schema import PAndamentoIdSchema


class ShowService:
    def execute(self, andamento_schema: PAndamentoIdSchema):
        return ShowAction().execute(andamento_schema)
