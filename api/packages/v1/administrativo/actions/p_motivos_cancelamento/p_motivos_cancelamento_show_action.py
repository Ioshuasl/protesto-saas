from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_motivos_cancelamento.p_motivos_cancelamento_show_repository import (
    ShowRepository,
)
from packages.v1.administrativo.schemas.p_motivos_cancelamento_schema import (
    PMotivosCancelamentoIdSchema,
)


class ShowAction(BaseAction):
    def execute(self, motivos_cancelamento_schema: PMotivosCancelamentoIdSchema):
        return ShowRepository().execute(motivos_cancelamento_schema)
