from packages.v1.nfse.actions.nfse_index_action import NfseIndexAction


class NfseIndexService:
    def execute(self):
        action = NfseIndexAction()
        return action.execute()
