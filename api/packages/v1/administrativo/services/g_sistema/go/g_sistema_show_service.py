from packages.v1.administrativo.actions.g_sistema.g_sistema_show_action import ShowAction
from packages.v1.administrativo.schemas.g_sistema_schema import GSistemaIdSchema


class ShowService:
    def execute(self, sistema_schema: GSistemaIdSchema):
        show_action = ShowAction()
        return show_action.execute(sistema_schema)
