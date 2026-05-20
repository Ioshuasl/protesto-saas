from abstracts.action import BaseAction
from packages.v1.nfse.repositories.parametros_index_repository import (
    ParametrosIndexRepository,
)


class ParametrosIndexAction(BaseAction):
    def execute(self):
        repository = ParametrosIndexRepository()
        return repository.execute()

