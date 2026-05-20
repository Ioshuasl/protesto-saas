from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_banco.p_banco_show_repository import (
    ShowRepository,
)
from packages.v1.administrativo.schemas.p_banco_schema import PBancoIdSchema


class ShowAction(BaseAction):
    def execute(self, banco_schema: PBancoIdSchema):
        return ShowRepository().execute(banco_schema)
