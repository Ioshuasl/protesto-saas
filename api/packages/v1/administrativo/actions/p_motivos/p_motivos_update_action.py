from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_motivos.p_motivos_update_repository import (
    UpdateRepository,
)
from packages.v1.administrativo.schemas.p_motivos_schema import PMotivosUpdateSchema


class UpdateAction(BaseAction):
    def execute(self, motivos_id: int, motivos_schema: PMotivosUpdateSchema):
        return UpdateRepository().execute(motivos_id, motivos_schema)
