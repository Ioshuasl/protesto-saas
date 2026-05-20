from abstracts.action import BaseAction
from packages.v1.nfse.repositories.parametros_last_repository import (
    ParametrosLastRepository,
)


class ParametrosLastAction(BaseAction):
    def execute(self):
        repository = ParametrosLastRepository()
        return repository.execute()

