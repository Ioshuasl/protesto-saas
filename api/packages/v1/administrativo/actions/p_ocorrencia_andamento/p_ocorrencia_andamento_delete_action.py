from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_ocorrencia_andamento.p_ocorrencia_andamento_delete_repository import (
    DeleteRepository,
)
from packages.v1.administrativo.schemas.p_ocorrencia_andamento_schema import (
    POcorrenciaAndamentoIdSchema,
)


class DeleteAction(BaseAction):
    def execute(self, ocorrencia_andamento_schema: POcorrenciaAndamentoIdSchema):
        return DeleteRepository().execute(ocorrencia_andamento_schema)
