from abstracts.action import BaseAction
from actions.data.query_params_parser import QueryParams
from packages.v1.administrativo.repositories.p_motivos.p_motivos_index_repository import (
    IndexRepository,
)
from packages.v1.administrativo.schemas.p_motivos_schema import PMotivosIndexSchema


class IndexAction(BaseAction):
    def execute(
        self,
        motivos_index_schema: PMotivosIndexSchema,
        query_params: QueryParams,
    ):
        return IndexRepository().execute(motivos_index_schema, query_params)
