from packages.v1.administrativo.actions.g_sistema.g_sistema_save_action import SaveAction
from packages.v1.administrativo.schemas.g_sistema_schema import GSistemaSaveSchema


class SaveService:
    def execute(self, sistema_schema: GSistemaSaveSchema):
        save_action = SaveAction()
        return save_action.execute(sistema_schema)
