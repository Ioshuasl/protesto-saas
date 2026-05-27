from abstracts.action import BaseAction
from actions.data.query_params_parser import QueryParams
from packages.v1.administrativo.repositories.p_titulo.p_titulo_index_somente_cadastrados_repository import (
    IndexSomenteCadastradosRepository,
)
from packages.v1.administrativo.schemas.p_titulo_schema import PTituloIndexSchema


class IndexSomenteCadastradosAction(BaseAction):
    def execute(
        self,
        titulo_index_schema: PTituloIndexSchema,
        query_params: QueryParams,
    ):
        return IndexSomenteCadastradosRepository().execute(
            titulo_index_schema, query_params
        )
