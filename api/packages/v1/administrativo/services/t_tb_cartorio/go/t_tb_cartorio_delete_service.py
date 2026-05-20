from packages.v1.administrativo.actions.t_tb_cartorio.t_tb_cartorio_delete_action import (
    TTbCartorioDeleteAction,
)
from packages.v1.administrativo.schemas.t_tb_cartorio_schema import TTbCartorioIdSchema
from packages.v1.administrativo.services.t_tb_cartorio.go.t_tb_cartorio_show_service import (
    TTbCartorioShowService,
)


class TTbCartorioDeleteService:
    def execute(self, cartorio_schema: TTbCartorioIdSchema):
        TTbCartorioShowService().execute(cartorio_schema)
        return TTbCartorioDeleteAction().execute(cartorio_schema)
