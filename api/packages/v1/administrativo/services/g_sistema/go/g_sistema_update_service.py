from typing import Union

from packages.v1.administrativo.actions.g_sistema.g_sistema_update_action import (
    UpdateAction,
)
from packages.v1.administrativo.schemas.g_sistema_schema import GSistemaUpdateSchema


class UpdateService:
    def execute(
        self,
        sistema_id: Union[int, float],
        sistema_schema: GSistemaUpdateSchema,
    ):
        update_action = UpdateAction()
        return update_action.execute(sistema_id, sistema_schema)
