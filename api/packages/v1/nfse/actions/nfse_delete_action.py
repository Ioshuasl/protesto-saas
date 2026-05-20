from abstracts.action import BaseAction
from packages.v1.nfse.repositories.nfse_delete_repository import NfseDeleteRepository
from packages.v1.nfse.schemas.nfse_schema import NfseIdSchema


class NfseDeleteAction(BaseAction):
    def execute(self, data: NfseIdSchema):
        repository = NfseDeleteRepository()
        return repository.execute(data)
