from actions.data.query_params_parser import QueryParams
from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_template.p_template_index_repository import (
    IndexRepository,
)
from packages.v1.administrativo.schemas.p_template_schema import PTemplateIndexSchema


class IndexAction(BaseAction):
    def execute(
        self,
        template_index_schema: PTemplateIndexSchema,
        query_params: QueryParams,
    ):
        return IndexRepository().execute(template_index_schema, query_params)
