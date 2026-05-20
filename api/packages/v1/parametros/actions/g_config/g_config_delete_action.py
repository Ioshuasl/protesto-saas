from abstracts.action import BaseAction
from packages.v1.parametros.repositories.g_config.g_config_delete_repository import (
    GConfigDeleteRepository,
)
from packages.v1.parametros.schemas.g_config_schema import GConfigIdSchema


class GConfigDeleteAction(BaseAction):
    def execute(self, data: GConfigIdSchema):
        repository = GConfigDeleteRepository()
        return repository.execute(data)
