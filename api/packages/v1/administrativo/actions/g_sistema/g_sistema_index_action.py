from actions.data.query_params_parser import QueryParams
from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_sistema.g_sistema_index_repository import (
    IndexRepository,
)
from packages.v1.administrativo.schemas.g_sistema_schema import GSistemaIndexSchema


class IndexAction(BaseAction):
    def execute(
        self,
        sistema_index_schema: GSistemaIndexSchema,
        query_params: QueryParams,
    ):
        return IndexRepository().execute(sistema_index_schema, query_params)
