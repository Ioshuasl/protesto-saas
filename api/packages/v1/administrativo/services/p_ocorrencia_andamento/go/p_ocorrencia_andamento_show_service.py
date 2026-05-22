from packages.v1.administrativo.actions.p_ocorrencia_andamento.p_ocorrencia_andamento_show_action import (
    ShowAction,
)
from packages.v1.administrativo.schemas.p_ocorrencia_andamento_schema import (
    POcorrenciaAndamentoIdSchema,
)


class ShowService:
    def execute(self, ocorrencia_andamento_schema: POcorrenciaAndamentoIdSchema):
        return ShowAction().execute(ocorrencia_andamento_schema)
