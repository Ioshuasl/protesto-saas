from packages.v1.administrativo.actions.p_ocorrencia_andamento.p_ocorrencia_andamento_index_action import (
    IndexAction,
)
from packages.v1.administrativo.schemas.p_ocorrencia_andamento_schema import (
    POcorrenciaAndamentoIndexSchema,
)
from actions.data.query_params_parser import QueryParams


class IndexService:
    def execute(
        self,
        ocorrencia_andamento_index_schema: POcorrenciaAndamentoIndexSchema,
        query_params: QueryParams,
    ):
        return IndexAction().execute(ocorrencia_andamento_index_schema, query_params)
