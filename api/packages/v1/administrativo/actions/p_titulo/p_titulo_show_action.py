from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_titulo.p_titulo_show_repository import (
    ShowRepository,
)
from packages.v1.administrativo.schemas.p_titulo_schema import PTituloIdSchema


class ShowAction(BaseAction):
    def execute(self, titulo_schema: PTituloIdSchema):
        return ShowRepository().execute(titulo_schema)
