from abstracts.action import BaseAction
from actions.data.query_params_parser import QueryParams
from packages.v1.administrativo.repositories.p_motivos_cancelamento.p_motivos_cancelamento_index_repository import (
    IndexRepository,
)
from packages.v1.administrativo.schemas.p_motivos_cancelamento_schema import (
    PMotivosCancelamentoIndexSchema,
)


class IndexAction(BaseAction):
    def execute(
        self,
        motivos_cancelamento_index_schema: PMotivosCancelamentoIndexSchema,
        query_params: QueryParams,
    ):
        return IndexRepository().execute(
            motivos_cancelamento_index_schema, query_params
        )
