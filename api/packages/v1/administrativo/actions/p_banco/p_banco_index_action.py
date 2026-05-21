from abstracts.action import BaseAction
from actions.data.query_params_parser import QueryParams
from packages.v1.administrativo.repositories.p_banco.p_banco_index_repository import (
    IndexRepository,
)
from packages.v1.administrativo.schemas.p_banco_schema import PBancoIndexSchema


class IndexAction(BaseAction):
    def execute(
        self,
        banco_index_schema: PBancoIndexSchema,
        query_params: QueryParams,
    ):
        return IndexRepository().execute(banco_index_schema, query_params)
