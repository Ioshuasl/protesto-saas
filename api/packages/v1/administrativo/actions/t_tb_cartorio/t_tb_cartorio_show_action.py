from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_tb_cartorio.t_tb_cartorio_show_repository import TTbCartorioShowRepository
from packages.v1.administrativo.schemas.t_tb_cartorio_schema import TTbCartorioIdSchema
class TTbCartorioShowAction(BaseAction):
    def execute(self, cartorio_schema: TTbCartorioIdSchema):
        return TTbCartorioShowRepository().execute(cartorio_schema)
