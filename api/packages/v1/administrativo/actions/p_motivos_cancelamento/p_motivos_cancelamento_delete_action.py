from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_motivos_cancelamento.p_motivos_cancelamento_delete_repository import (
    DeleteRepository,
)
from packages.v1.administrativo.schemas.p_motivos_cancelamento_schema import (
    PMotivosCancelamentoIdSchema,
)


class DeleteAction(BaseAction):
    def execute(self, motivos_cancelamento_schema: PMotivosCancelamentoIdSchema):
        return DeleteRepository().execute(motivos_cancelamento_schema)
