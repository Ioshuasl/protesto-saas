from actions.data.query_params_parser import QueryParams
from packages.v1.administrativo.actions.p_template.p_template_index_action import (
    IndexAction,
)
from packages.v1.administrativo.schemas.p_template_schema import PTemplateIndexSchema


class IndexService:
    def execute(
        self,
        template_index_schema: PTemplateIndexSchema,
        query_params: QueryParams,
    ):
        return IndexAction().execute(template_index_schema, query_params)
