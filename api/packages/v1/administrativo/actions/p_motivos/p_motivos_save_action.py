from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_motivos.p_motivos_save_repository import (
    SaveRepository,
)
from packages.v1.administrativo.schemas.p_motivos_schema import PMotivosSaveSchema


class SaveAction(BaseAction):
    def execute(self, motivos_schema: PMotivosSaveSchema):
        return SaveRepository().execute(motivos_schema)
