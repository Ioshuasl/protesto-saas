from abstracts.action import BaseAction
from packages.v1.parametros.repositories.g_config.g_config_save_repository import (
    GConfigSaveRepository,
)
from packages.v1.parametros.schemas.g_config_schema import GConfigSaveSchema


class GConfigSaveAction(BaseAction):
    def execute(self, data: GConfigSaveSchema):
        repository = GConfigSaveRepository()
        return repository.execute(data)
