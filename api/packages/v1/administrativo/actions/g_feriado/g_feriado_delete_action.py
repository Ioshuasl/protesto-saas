from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_feriado.g_feriado_delete_repository import (
    DeleteRepository,
)
from packages.v1.administrativo.schemas.g_feriado_schema import GFeriadoIdSchema


class DeleteAction(BaseAction):
    def execute(self, feriado_schema: GFeriadoIdSchema):
        return DeleteRepository().execute(feriado_schema)
