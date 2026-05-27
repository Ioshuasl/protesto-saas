from abstracts.action import BaseAction
from actions.data.query_params_parser import QueryParams
from packages.v1.administrativo.repositories.p_titulo.p_titulo_index_somente_apontados_repository import (
    IndexSomenteApontadosRepository,
)
from packages.v1.administrativo.schemas.p_titulo_schema import PTituloIndexSchema


class IndexSomenteApontadosAction(BaseAction):
    def execute(
        self,
        titulo_index_schema: PTituloIndexSchema,
        query_params: QueryParams,
    ):
        return IndexSomenteApontadosRepository().execute(titulo_index_schema, query_params)
