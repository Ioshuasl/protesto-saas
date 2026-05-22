from abstracts.action import BaseAction
from actions.data.query_params_parser import QueryParams
from packages.v1.administrativo.repositories.p_andamento.p_andamento_index_repository import (
    IndexRepository,
)
from packages.v1.administrativo.schemas.p_andamento_schema import PAndamentoIndexSchema


class IndexAction(BaseAction):
    def execute(
        self,
        andamento_index_schema: PAndamentoIndexSchema,
        query_params: QueryParams,
    ):
        return IndexRepository().execute(andamento_index_schema, query_params)
