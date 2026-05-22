from actions.data.query_params_parser import QueryParams
from packages.v1.administrativo.actions.p_pessoa.p_pessoa_index_action import IndexAction
from packages.v1.administrativo.schemas.p_pessoa_schema import PPessoaIndexSchema


class IndexService:
    def execute(
        self,
        pessoa_index_schema: PPessoaIndexSchema,
        query_params: QueryParams,
    ):
        return IndexAction().execute(pessoa_index_schema, query_params)
