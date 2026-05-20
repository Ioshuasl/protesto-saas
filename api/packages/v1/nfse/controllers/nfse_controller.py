from packages.v1.nfse.schemas.nfse_schema import NfseIdSchema, NfseSaveSchema
from packages.v1.nfse.services.nfse_delete_service import NfseDeleteService
from packages.v1.nfse.services.nfse_index_service import NfseIndexService
from packages.v1.nfse.services.nfse_save_service import NfseSaveService
from packages.v1.nfse.services.nfse_show_service import NfseShowService


class NfseController:
    def index(self):
        service = NfseIndexService()
        return {
            "message": "NFS-e localizadas com sucesso",
            "data": service.execute(),
        }

    def show(self, data: NfseIdSchema):
        service = NfseShowService()
        return {
            "message": "NFS-e localizada com sucesso",
            "data": service.execute(data),
        }

    def save(self, data: NfseSaveSchema):
        service = NfseSaveService()
        return {
            "message": "NFS-e salva com sucesso",
            "data": service.execute(data),
        }

    def delete(self, data: NfseIdSchema):
        service = NfseDeleteService()
        return {
            "message": "NFS-e removida com sucesso",
            "data": service.execute(data),
        }
