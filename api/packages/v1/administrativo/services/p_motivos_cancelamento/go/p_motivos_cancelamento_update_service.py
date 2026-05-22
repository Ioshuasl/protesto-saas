from packages.v1.administrativo.actions.p_motivos_cancelamento.p_motivos_cancelamento_update_action import (
    UpdateAction,
)
from packages.v1.administrativo.schemas.p_motivos_cancelamento_schema import (
    PMotivosCancelamentoUpdateSchema,
)


class UpdateService:
    def execute(
        self,
        motivos_cancelamento_id: int,
        motivos_cancelamento_schema: PMotivosCancelamentoUpdateSchema,
    ):
        return UpdateAction().execute(
            motivos_cancelamento_id, motivos_cancelamento_schema
        )
