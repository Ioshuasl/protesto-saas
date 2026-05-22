from abstracts.action import BaseAction
from actions.data.query_params_parser import QueryParams
from packages.v1.administrativo.repositories.p_andamento.p_andamento_index_by_titulo_repository import (
    IndexByTituloRepository,
)
from packages.v1.administrativo.schemas.p_andamento_schema import PAndamentoIndexByTituloSchema


class IndexByTituloAction(BaseAction):
    def execute(
        self,
        titulo_id: int,
        filter_schema: PAndamentoIndexByTituloSchema,
        query_params: QueryParams,
    ):
        return IndexByTituloRepository().execute(titulo_id, filter_schema, query_params)
