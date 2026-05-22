from packages.v1.administrativo.actions.p_motivos_cancelamento.p_motivos_cancelamento_show_action import (
    ShowAction,
)
from packages.v1.administrativo.schemas.p_motivos_cancelamento_schema import (
    PMotivosCancelamentoIdSchema,
)


class ShowService:
    def execute(self, motivos_cancelamento_schema: PMotivosCancelamentoIdSchema):
        return ShowAction().execute(motivos_cancelamento_schema)
