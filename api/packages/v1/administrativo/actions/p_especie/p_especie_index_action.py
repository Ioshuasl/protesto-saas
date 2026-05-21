from abstracts.action import BaseAction
from actions.data.query_params_parser import QueryParams
from packages.v1.administrativo.repositories.p_especie.p_especie_index_repository import (
    IndexRepository,
)
from packages.v1.administrativo.schemas.p_especie_schema import PEspecieIndexSchema


class IndexAction(BaseAction):
    def execute(
        self,
        especie_index_schema: PEspecieIndexSchema,
        query_params: QueryParams,
    ):
        return IndexRepository().execute(especie_index_schema, query_params)
