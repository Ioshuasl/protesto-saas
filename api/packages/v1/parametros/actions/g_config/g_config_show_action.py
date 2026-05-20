from abstracts.action import BaseAction
from packages.v1.parametros.repositories.g_config.g_config_show_repository import (
    GConfigShowRepository,
)
from packages.v1.parametros.schemas.g_config_schema import GConfigIdSchema


class GConfigShowAction(BaseAction):
    def execute(self, g_config_schema: GConfigIdSchema):
        show_repository = GConfigShowRepository()

        response = show_repository.execute(g_config_schema)
        return response
