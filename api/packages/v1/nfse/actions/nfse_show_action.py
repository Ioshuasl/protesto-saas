from abstracts.action import BaseAction
from packages.v1.nfse.repositories.nfse_show_repository import NfseShowRepository
from packages.v1.nfse.schemas.nfse_schema import NfseIdSchema


class NfseShowAction(BaseAction):
    def execute(self, data: NfseIdSchema):
        repository = NfseShowRepository()
        return repository.execute(data)
