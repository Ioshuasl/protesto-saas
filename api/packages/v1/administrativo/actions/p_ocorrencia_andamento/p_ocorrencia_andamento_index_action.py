from abstracts.action import BaseAction
from actions.data.query_params_parser import QueryParams
from packages.v1.administrativo.repositories.p_ocorrencia_andamento.p_ocorrencia_andamento_index_repository import (
    IndexRepository,
)
from packages.v1.administrativo.schemas.p_ocorrencia_andamento_schema import (
    POcorrenciaAndamentoIndexSchema,
)


class IndexAction(BaseAction):
    def execute(
        self,
        ocorrencia_andamento_index_schema: POcorrenciaAndamentoIndexSchema,
        query_params: QueryParams,
    ):
        return IndexRepository().execute(ocorrencia_andamento_index_schema, query_params)
