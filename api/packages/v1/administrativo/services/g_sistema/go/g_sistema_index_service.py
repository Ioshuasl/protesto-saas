from actions.data.query_params_parser import QueryParams
from packages.v1.administrativo.actions.g_sistema.g_sistema_index_action import IndexAction
from packages.v1.administrativo.schemas.g_sistema_schema import GSistemaIndexSchema


class IndexService:
    def execute(
        self,
        sistema_index_schema: GSistemaIndexSchema,
        query_params: QueryParams,
    ):
        index_action = IndexAction()
        return index_action.execute(sistema_index_schema, query_params)
