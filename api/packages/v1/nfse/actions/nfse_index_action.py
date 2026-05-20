from abstracts.action import BaseAction
from packages.v1.nfse.repositories.nfse_index_repository import NfseIndexRepository


class NfseIndexAction(BaseAction):
    def execute(self):
        repository = NfseIndexRepository()
        return repository.execute()
