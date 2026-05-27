from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_sistema.g_sistema_delete_repository import (
    DeleteRepository,
)
from packages.v1.administrativo.schemas.g_sistema_schema import GSistemaIdSchema


class DeleteAction(BaseAction):
    def execute(self, sistema_schema: GSistemaIdSchema):
        return DeleteRepository().execute(sistema_schema)
