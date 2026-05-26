from packages.v1.administrativo.actions.p_certidao.p_certidao_show_action import (
    ShowAction,
)
from packages.v1.administrativo.actions.p_certidao.p_certidao_update_action import (
    UpdateAction,
)
from packages.v1.administrativo.schemas.p_certidao_schema import (
    PCertidaoIdSchema,
    PCertidaoUpdateSchema,
)


class UpdateService:
    def execute(self, certidao_id: int, certidao_schema: PCertidaoUpdateSchema):
        ShowAction().execute(PCertidaoIdSchema(certidao_id=certidao_id))
        return UpdateAction().execute(certidao_id, certidao_schema)
