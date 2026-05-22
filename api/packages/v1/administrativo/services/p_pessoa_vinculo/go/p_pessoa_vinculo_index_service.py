from actions.data.query_params_parser import QueryParams
from packages.v1.administrativo.actions.p_pessoa_vinculo.p_pessoa_vinculo_index_action import (
    IndexAction,
)
from packages.v1.administrativo.schemas.p_pessoa_vinculo_schema import PPessoaVinculoIndexSchema


class IndexService:
    def execute(
        self,
        vinculo_index_schema: PPessoaVinculoIndexSchema,
        query_params: QueryParams,
    ):
        return IndexAction().execute(vinculo_index_schema, query_params)
