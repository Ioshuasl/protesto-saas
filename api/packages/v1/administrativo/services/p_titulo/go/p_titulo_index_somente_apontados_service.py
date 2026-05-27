from actions.data.query_params_parser import QueryParams
from packages.v1.administrativo.actions.p_titulo.p_titulo_index_somente_apontados_action import (
    IndexSomenteApontadosAction,
)
from packages.v1.administrativo.schemas.p_titulo_schema import PTituloIndexSchema


class IndexSomenteApontadosService:
    def execute(
        self,
        titulo_index_schema: PTituloIndexSchema,
        query_params: QueryParams,
    ):
        return IndexSomenteApontadosAction().execute(titulo_index_schema, query_params)
