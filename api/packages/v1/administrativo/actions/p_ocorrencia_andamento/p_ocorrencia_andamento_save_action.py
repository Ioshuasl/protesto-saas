from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_ocorrencia_andamento.p_ocorrencia_andamento_save_repository import (
    SaveRepository,
)
from packages.v1.administrativo.schemas.p_ocorrencia_andamento_schema import (
    POcorrenciaAndamentoSaveSchema,
)


class SaveAction(BaseAction):
    def execute(self, ocorrencia_andamento_schema: POcorrenciaAndamentoSaveSchema):
        return SaveRepository().execute(ocorrencia_andamento_schema)
