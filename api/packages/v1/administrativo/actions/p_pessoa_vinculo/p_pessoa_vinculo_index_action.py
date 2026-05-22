from abstracts.action import BaseAction
from actions.data.query_params_parser import QueryParams
from packages.v1.administrativo.repositories.p_pessoa_vinculo.p_pessoa_vinculo_index_repository import (
    IndexRepository,
)
from packages.v1.administrativo.schemas.p_pessoa_vinculo_schema import PPessoaVinculoIndexSchema


class IndexAction(BaseAction):
    def execute(
        self,
        vinculo_index_schema: PPessoaVinculoIndexSchema,
        query_params: QueryParams,
    ):
        return IndexRepository().execute(vinculo_index_schema, query_params)
