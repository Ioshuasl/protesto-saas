from abstracts.action import BaseAction
from actions.data.query_params_parser import QueryParams
from packages.v1.administrativo.repositories.p_certidao.p_certidao_index_repository import (
    IndexRepository,
)
from packages.v1.administrativo.schemas.p_certidao_schema import PCertidaoIndexSchema


class IndexAction(BaseAction):
    def execute(
        self,
        certidao_index_schema: PCertidaoIndexSchema,
        query_params: QueryParams,
    ):
        return IndexRepository().execute(certidao_index_schema, query_params)
