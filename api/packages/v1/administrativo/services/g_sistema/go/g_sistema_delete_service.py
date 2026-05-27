from packages.v1.administrativo.actions.g_sistema.g_sistema_delete_action import (
    DeleteAction,
)
from packages.v1.administrativo.schemas.g_sistema_schema import GSistemaIdSchema


class DeleteService:
    def execute(self, sistema_schema: GSistemaIdSchema):
        delete_action = DeleteAction()
        return delete_action.execute(sistema_schema)
