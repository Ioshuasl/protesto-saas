from abstracts.action import BaseAction
from packages.v1.nfse.repositories.nfse_save_repository import NfseSaveRepository
from packages.v1.nfse.schemas.nfse_schema import NfseSaveSchema


class NfseSaveAction(BaseAction):
    def execute(self, data: NfseSaveSchema):
        repository = NfseSaveRepository()
        return repository.execute(data)
