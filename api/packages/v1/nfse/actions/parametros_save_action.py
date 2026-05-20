from abstracts.action import BaseAction
from packages.v1.nfse.repositories.parametros_save_repository import (
    ParametrosSaveRepository,
)
from packages.v1.nfse.schemas.parametros_schema import ParametrosSaveSchema


class ParametrosSaveAction(BaseAction):
    def execute(self, data: ParametrosSaveSchema):
        repository = ParametrosSaveRepository()
        return repository.execute(data)

