from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_certidao.p_certidao_show_repository import (
    ShowRepository,
)
from packages.v1.administrativo.schemas.p_certidao_schema import PCertidaoIdSchema


class ShowAction(BaseAction):
    def execute(self, certidao_schema: PCertidaoIdSchema):
        return ShowRepository().execute(certidao_schema)
