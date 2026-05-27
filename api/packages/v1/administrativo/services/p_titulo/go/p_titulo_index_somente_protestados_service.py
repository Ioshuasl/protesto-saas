from actions.data.query_params_parser import QueryParams
from packages.v1.administrativo.actions.p_titulo.p_titulo_index_somente_protestados_action import (
    IndexSomenteProtestadosAction,
)
from packages.v1.administrativo.schemas.p_titulo_schema import PTituloIndexSchema


class IndexSomenteProtestadosService:
    def execute(
        self,
        titulo_index_schema: PTituloIndexSchema,
        query_params: QueryParams,
    ):
        return IndexSomenteProtestadosAction().execute(titulo_index_schema, query_params)
