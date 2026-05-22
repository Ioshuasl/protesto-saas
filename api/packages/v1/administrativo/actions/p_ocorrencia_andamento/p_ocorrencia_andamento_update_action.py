from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_ocorrencia_andamento.p_ocorrencia_andamento_update_repository import (
    UpdateRepository,
)
from packages.v1.administrativo.schemas.p_ocorrencia_andamento_schema import (
    POcorrenciaAndamentoUpdateSchema,
)


class UpdateAction(BaseAction):
    def execute(
        self,
        ocorrencia_andamento_id: int,
        ocorrencia_andamento_schema: POcorrenciaAndamentoUpdateSchema,
    ):
        return UpdateRepository().execute(
            ocorrencia_andamento_id, ocorrencia_andamento_schema
        )
