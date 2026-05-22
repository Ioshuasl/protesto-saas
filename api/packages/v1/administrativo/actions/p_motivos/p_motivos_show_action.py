from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_motivos.p_motivos_show_repository import (
    ShowRepository,
)
from packages.v1.administrativo.schemas.p_motivos_schema import PMotivosIdSchema


class ShowAction(BaseAction):
    def execute(self, motivos_schema: PMotivosIdSchema):
        return ShowRepository().execute(motivos_schema)
