from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_ocorrencia_andamento.p_ocorrencia_andamento_show_repository import (
    ShowRepository,
)
from packages.v1.administrativo.schemas.p_ocorrencia_andamento_schema import (
    POcorrenciaAndamentoIdSchema,
)


class ShowAction(BaseAction):
    def execute(self, ocorrencia_andamento_schema: POcorrenciaAndamentoIdSchema):
        return ShowRepository().execute(ocorrencia_andamento_schema)
