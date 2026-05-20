from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_feriado.g_feriado_update_repository import (
    UpdateRepository,
)
from packages.v1.administrativo.schemas.g_feriado_schema import GFeriadoUpdateSchema


class UpdateAction(BaseAction):
    def execute(self, feriado_id: int, feriado_schema: GFeriadoUpdateSchema):
        return UpdateRepository().execute(feriado_id, feriado_schema)
