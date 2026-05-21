from actions.data.query_params_parser import QueryParams
from packages.v1.administrativo.actions.g_feriado.g_feriado_index_action import IndexAction
from packages.v1.administrativo.schemas.g_feriado_schema import GFeriadoIndexSchema


class IndexService:
    def execute(
        self,
        feriado_index_schema: GFeriadoIndexSchema,
        query_params: QueryParams,
    ):
        index_action = IndexAction()
        return index_action.execute(feriado_index_schema, query_params)
