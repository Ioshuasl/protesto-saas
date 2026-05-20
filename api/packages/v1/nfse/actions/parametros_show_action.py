from abstracts.action import BaseAction
from packages.v1.nfse.repositories.parametros_show_repository import (
    ParametrosShowRepository,
)
from packages.v1.nfse.schemas.parametros_schema import ParametrosIdSchema


class ParametrosShowAction(BaseAction):
    def execute(self, data: ParametrosIdSchema):
        repository = ParametrosShowRepository()
        return repository.execute(data)

