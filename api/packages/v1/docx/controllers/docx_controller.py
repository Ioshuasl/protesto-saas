from packages.v1.docx.schemas.docx_schema import DOCXSchemaCallback
from packages.v1.docx.services.docx_save_service import DOCXSaveService


class DOCXController:

    # Lista todos os regimes de bens
    def save(self, data: DOCXSchemaCallback):

        # Executa o serviço desejado
        response = DOCXSaveService().execute(data)

        # Lista todos os regimes de bens
        return {
            "message": "Texto salvo com sucesso",
            "data": response,
        }
