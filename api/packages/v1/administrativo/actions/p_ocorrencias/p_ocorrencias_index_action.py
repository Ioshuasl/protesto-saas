from abstracts.action import BaseAction
from actions.data.query_params_parser import QueryParams
from packages.v1.administrativo.repositories.p_ocorrencias.p_ocorrencias_index_repository import (
    IndexRepository,
)
from packages.v1.administrativo.schemas.p_ocorrencias_schema import POcorrenciasIndexSchema


class IndexAction(BaseAction):
    def execute(
        self,
        ocorrencias_index_schema: POcorrenciasIndexSchema,
        query_params: QueryParams,
    ):
        return IndexRepository().execute(ocorrencias_index_schema, query_params)
