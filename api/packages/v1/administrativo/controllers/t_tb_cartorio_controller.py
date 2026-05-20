from packages.v1.administrativo.schemas.t_tb_cartorio_schema import (
    TTbCartorioIdSchema,
    TTbCartorioSaveSchema,
)
from packages.v1.administrativo.services.t_tb_cartorio.go.t_tb_cartorio_delete_service import (
    TTbCartorioDeleteService,
)
from packages.v1.administrativo.services.t_tb_cartorio.go.t_tb_cartorio_index_service import (
    TTbCartorioIndexService,
)
from packages.v1.administrativo.services.t_tb_cartorio.go.t_tb_cartorio_save_service import (
    TTbCartorioSaveService,
)
from packages.v1.administrativo.services.t_tb_cartorio.go.t_tb_cartorio_show_service import (
    TTbCartorioShowService,
)


class TTbCartorioController:
    def index(self):
        return {
            "message": "Cartorios localizados com sucesso",
            "data": TTbCartorioIndexService().execute(),
        }

    def show(self, cartorio_schema: TTbCartorioIdSchema):
        return {
            "message": "Cartorio localizado com sucesso",
            "data": TTbCartorioShowService().execute(cartorio_schema),
        }

    def save(self, cartorio_schema: TTbCartorioSaveSchema):
        return {
            "message": "Cartorio salvo com sucesso",
            "data": TTbCartorioSaveService().execute(cartorio_schema),
        }

    def delete(self, cartorio_schema: TTbCartorioIdSchema):
        return {
            "message": "Cartorio removido com sucesso",
            "data": TTbCartorioDeleteService().execute(cartorio_schema),
        }
