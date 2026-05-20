from packages.v1.nfse.schemas.parametros_schema import (
    ParametrosIdSchema,
    ParametrosSaveSchema,
)
from packages.v1.nfse.services.parametros_delete_service import ParametrosDeleteService
from packages.v1.nfse.services.parametros_index_service import ParametrosIndexService
from packages.v1.nfse.services.parametros_save_service import ParametrosSaveService
from packages.v1.nfse.services.parametros_show_service import ParametrosShowService


class ParametrosController:
    def index(self):
        service = ParametrosIndexService()
        return {
            "message": "Parametros localizados com sucesso",
            "data": service.execute(),
        }

    def show(self, data: ParametrosIdSchema):
        service = ParametrosShowService()
        return {
            "message": "Parametros localizados com sucesso",
            "data": service.execute(data),
        }

    def save(self, data: ParametrosSaveSchema):
        service = ParametrosSaveService()
        return {
            "message": "Parametros salvos com sucesso",
            "data": service.execute(data),
        }

    def delete(self, data: ParametrosIdSchema):
        service = ParametrosDeleteService()
        return {
            "message": "Parametros removidos com sucesso",
            "data": service.execute(data),
        }

