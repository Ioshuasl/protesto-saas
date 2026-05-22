from actions.data.query_params_parser import QueryParams
from packages.v1.administrativo.actions.p_ocorrencias.p_ocorrencias_index_action import (
    IndexAction,
)
from packages.v1.administrativo.schemas.p_ocorrencias_schema import POcorrenciasIndexSchema


class IndexService:
    def execute(
        self,
        ocorrencias_index_schema: POcorrenciasIndexSchema,
        query_params: QueryParams,
    ):
        return IndexAction().execute(ocorrencias_index_schema, query_params)
