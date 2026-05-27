from actions.data.query_params_parser import QueryParams
from packages.v1.administrativo.actions.p_titulo.p_titulo_index_somente_intimados_action import (
    IndexSomenteIntimadosAction,
)
from packages.v1.administrativo.schemas.p_titulo_schema import PTituloIndexSchema


class IndexSomenteIntimadosService:
    def execute(
        self,
        titulo_index_schema: PTituloIndexSchema,
        query_params: QueryParams,
    ):
        return IndexSomenteIntimadosAction().execute(titulo_index_schema, query_params)
