from actions.data.query_params_parser import QueryParams
from packages.v1.administrativo.actions.p_certidao.p_certidao_index_action import (
    IndexAction,
)
from packages.v1.administrativo.schemas.p_certidao_schema import PCertidaoIndexSchema


class IndexService:
    def execute(
        self,
        certidao_index_schema: PCertidaoIndexSchema,
        query_params: QueryParams,
    ):
        return IndexAction().execute(certidao_index_schema, query_params)
