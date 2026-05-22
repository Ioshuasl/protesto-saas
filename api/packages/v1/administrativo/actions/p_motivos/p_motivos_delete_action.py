from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_motivos.p_motivos_delete_repository import (
    DeleteRepository,
)
from packages.v1.administrativo.schemas.p_motivos_schema import PMotivosIdSchema


class DeleteAction(BaseAction):
    def execute(self, motivos_schema: PMotivosIdSchema):
        return DeleteRepository().execute(motivos_schema)
