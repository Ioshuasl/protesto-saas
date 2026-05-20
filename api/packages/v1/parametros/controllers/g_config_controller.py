from packages.v1.parametros.schemas.g_config_schema import (
    GConfigIdSchema,
    GConfigIndexFilterSchema,
    GConfigSaveSchema,
)
from packages.v1.parametros.services.g_config.go.g_config_delete_service import (
    GConfigDeleteService,
)
from packages.v1.parametros.services.g_config.go.g_config_index_service import (
    GConfigIndexService,
)
from packages.v1.parametros.services.g_config.go.g_config_save_service import (
    GConfigSaveService,
)
from packages.v1.parametros.services.g_config.go.g_config_show_service import (
    GConfigShowService,
)


class GConfigController:
    def index(self, data: GConfigIndexFilterSchema):
        service = GConfigIndexService()
        return {
            "message": "G_CONFIG localizados com sucesso",
            "data": service.execute(data),
        }

    def show(self, data: GConfigIdSchema):
        service = GConfigShowService()
        response = service.execute(data)
        return {
            "message": "G_CONFIG localizado com sucesso",
            "data": response,
        }

    def save(self, data: GConfigSaveSchema):
        service = GConfigSaveService()
        return {
            "message": "G_CONFIG salvo com sucesso",
            "data": service.execute(data),
        }

    def delete(self, data: GConfigIdSchema):
        service = GConfigDeleteService()
        return {
            "message": "G_CONFIG removido com sucesso",
            "data": service.execute(data),
        }
