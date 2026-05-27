from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_sistema.g_sistema_show_repository import (
    ShowRepository,
)
from packages.v1.administrativo.schemas.g_sistema_schema import GSistemaIdSchema


class ShowAction(BaseAction):
    def execute(self, sistema_schema: GSistemaIdSchema):
        return ShowRepository().execute(sistema_schema)
