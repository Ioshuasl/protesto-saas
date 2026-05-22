from actions.data.query_params_parser import QueryParams
from packages.v1.administrativo.actions.p_motivos.p_motivos_index_action import IndexAction
from packages.v1.administrativo.schemas.p_motivos_schema import PMotivosIndexSchema


class IndexService:
    def execute(
        self,
        motivos_index_schema: PMotivosIndexSchema,
        query_params: QueryParams,
    ):
        return IndexAction().execute(motivos_index_schema, query_params)
