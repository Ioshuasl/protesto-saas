from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_tb_cartorio.t_tb_cartorio_delete_repository import TTbCartorioDeleteRepository
from packages.v1.administrativo.schemas.t_tb_cartorio_schema import TTbCartorioIdSchema
class TTbCartorioDeleteAction(BaseAction):
    def execute(self, cartorio_schema: TTbCartorioIdSchema):
        return TTbCartorioDeleteRepository().execute(cartorio_schema)
