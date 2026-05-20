from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_feriado.g_feriado_save_repository import (
    SaveRepository,
)
from packages.v1.administrativo.schemas.g_feriado_schema import GFeriadoSaveSchema


class SaveAction(BaseAction):
    def execute(self, feriado_schema: GFeriadoSaveSchema):
        return SaveRepository().execute(feriado_schema)
