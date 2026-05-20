from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_feriado.g_feriado_show_repository import (
    ShowRepository,
)
from packages.v1.administrativo.schemas.g_feriado_schema import GFeriadoIdSchema


class ShowAction(BaseAction):
    def execute(self, feriado_schema: GFeriadoIdSchema):
        return ShowRepository().execute(feriado_schema)
