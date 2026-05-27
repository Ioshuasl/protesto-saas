from typing import Union

from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_sistema.g_sistema_update_repository import (
    UpdateRepository,
)
from packages.v1.administrativo.schemas.g_sistema_schema import GSistemaUpdateSchema


class UpdateAction(BaseAction):
    def execute(
        self,
        sistema_id: Union[int, float],
        sistema_schema: GSistemaUpdateSchema,
    ):
        return UpdateRepository().execute(sistema_id, sistema_schema)
