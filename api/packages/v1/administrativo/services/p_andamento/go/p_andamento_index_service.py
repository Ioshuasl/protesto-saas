from actions.data.query_params_parser import QueryParams
from packages.v1.administrativo.actions.p_andamento.p_andamento_index_action import (
    IndexAction,
)
from packages.v1.administrativo.schemas.p_andamento_schema import PAndamentoIndexSchema


class IndexService:
    def execute(
        self,
        andamento_index_schema: PAndamentoIndexSchema,
        query_params: QueryParams,
    ):
        return IndexAction().execute(andamento_index_schema, query_params)
