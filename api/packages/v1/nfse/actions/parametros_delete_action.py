from abstracts.action import BaseAction
from packages.v1.nfse.repositories.parametros_delete_repository import (
    ParametrosDeleteRepository,
)
from packages.v1.nfse.schemas.parametros_schema import ParametrosIdSchema


class ParametrosDeleteAction(BaseAction):
    def execute(self, data: ParametrosIdSchema):
        repository = ParametrosDeleteRepository()
        return repository.execute(data)

