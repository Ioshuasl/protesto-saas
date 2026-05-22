from actions.data.query_params_parser import QueryParams
from packages.v1.administrativo.actions.p_motivos_cancelamento.p_motivos_cancelamento_index_action import (
    IndexAction,
)
from packages.v1.administrativo.schemas.p_motivos_cancelamento_schema import (
    PMotivosCancelamentoIndexSchema,
)


class IndexService:
    def execute(
        self,
        motivos_cancelamento_index_schema: PMotivosCancelamentoIndexSchema,
        query_params: QueryParams,
    ):
        return IndexAction().execute(motivos_cancelamento_index_schema, query_params)
