from actions.data.query_params_parser import QueryParams
from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_pessoa.p_pessoa_index_repository import (
    IndexRepository,
)
from packages.v1.administrativo.schemas.p_pessoa_schema import PPessoaIndexSchema


class IndexAction(BaseAction):
    def execute(
        self,
        pessoa_index_schema: PPessoaIndexSchema,
        query_params: QueryParams,
    ):
        return IndexRepository().execute(pessoa_index_schema, query_params)
