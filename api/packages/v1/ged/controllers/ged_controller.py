from packages.v1.ged.schemas.ged_schema import (
    GEDIndexSchema,
    GEDSaveBase64RequestSchema,
    GEDSaveMultipartRequestSchema,
    GEDSaveSchema,
)
from packages.v1.ged.services.ged_delete_service import GEDDeleteService
from packages.v1.ged.services.ged_index_service import GEDIndexService
from packages.v1.ged.services.ged_save_base64_service import GEDSaveBase64Service
from packages.v1.ged.services.ged_save_multipart_service import GEDSaveMultipartService
from packages.v1.ged.services.ged_save_service import GEDSaveService


class GEDController:
    def index(self, data: GEDIndexSchema):
        index_service = GEDIndexService()
        return {
            "message": "Registros localizados com sucesso",
            "data": index_service.execute(data),
        }

    def save(self, data: GEDSaveSchema):
        save_service = GEDSaveService()
        return {
            "message": "Registro salvo com sucesso",
            "data": save_service.execute(data),
        }

    async def save_base64(self, data: GEDSaveBase64RequestSchema):
        service = GEDSaveBase64Service()
        return {
            "message": "Registro salvo com sucesso",
            "data": await service.execute(data),
        }

    async def save_multipart(self, data: GEDSaveMultipartRequestSchema):
        service = GEDSaveMultipartService()
        return {
            "message": "Registro salvo com sucesso",
            "data": await service.execute(data),
        }

    def delete(self, data: GEDIndexSchema):
        delete_service = GEDDeleteService()
        return {
            "message": "Registro removido com sucesso",
            "data": delete_service.execute(data),
        }
