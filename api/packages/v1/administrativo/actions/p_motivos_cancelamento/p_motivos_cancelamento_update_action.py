from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_motivos_cancelamento.p_motivos_cancelamento_update_repository import (
    UpdateRepository,
)
from packages.v1.administrativo.schemas.p_motivos_cancelamento_schema import (
    PMotivosCancelamentoUpdateSchema,
)


class UpdateAction(BaseAction):
    def execute(
        self,
        motivos_cancelamento_id: int,
        motivos_cancelamento_schema: PMotivosCancelamentoUpdateSchema,
    ):
        return UpdateRepository().execute(
            motivos_cancelamento_id, motivos_cancelamento_schema
        )
