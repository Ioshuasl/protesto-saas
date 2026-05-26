from packages.v1.administrativo.actions.p_certidao.p_certidao_show_action import (
    ShowAction,
)
from packages.v1.administrativo.schemas.p_certidao_schema import PCertidaoIdSchema


class ShowService:
    def execute(self, certidao_schema: PCertidaoIdSchema):
        return ShowAction().execute(certidao_schema)
