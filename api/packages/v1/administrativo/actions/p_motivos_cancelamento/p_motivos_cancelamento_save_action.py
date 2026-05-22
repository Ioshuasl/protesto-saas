from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_motivos_cancelamento.p_motivos_cancelamento_save_repository import (
    SaveRepository,
)
from packages.v1.administrativo.schemas.p_motivos_cancelamento_schema import (
    PMotivosCancelamentoSaveSchema,
)


class SaveAction(BaseAction):
    def execute(self, motivos_cancelamento_schema: PMotivosCancelamentoSaveSchema):
        return SaveRepository().execute(motivos_cancelamento_schema)
