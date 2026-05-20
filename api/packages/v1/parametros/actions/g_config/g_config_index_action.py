from abstracts.action import BaseAction
from packages.v1.parametros.repositories.g_config.g_config_index_repository import (
    GConfigIndexRepository,
)
from packages.v1.parametros.schemas.g_config_schema import GConfigIndexFilterSchema


class GConfigIndexAction(BaseAction):
    def execute(self, data: GConfigIndexFilterSchema):
        repository = GConfigIndexRepository()
        return repository.execute(data)
