from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_sistema.g_sistema_save_repository import (
    SaveRepository,
)
from packages.v1.administrativo.schemas.g_sistema_schema import GSistemaSaveSchema


class SaveAction(BaseAction):
    def execute(self, sistema_schema: GSistemaSaveSchema):
        return SaveRepository().execute(sistema_schema)
