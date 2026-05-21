from actions.data.query_params_parser import QueryParams
from packages.v1.administrativo.actions.p_especie.p_especie_index_action import IndexAction
from packages.v1.administrativo.schemas.p_especie_schema import PEspecieIndexSchema


class IndexService:
    def execute(
        self,
        especie_index_schema: PEspecieIndexSchema,
        query_params: QueryParams,
    ):
        return IndexAction().execute(especie_index_schema, query_params)
