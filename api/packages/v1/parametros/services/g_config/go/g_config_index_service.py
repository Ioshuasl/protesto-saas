from packages.v1.parametros.actions.g_config.g_config_index_action import (
    GConfigIndexAction,
)
from packages.v1.parametros.schemas.g_config_schema import GConfigIndexFilterSchema


class GConfigIndexService:
    def execute(self, data: GConfigIndexFilterSchema):
        action = GConfigIndexAction()
        return action.execute(data)
