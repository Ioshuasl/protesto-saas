from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_tb_cartorio.t_tb_cartorio_save_repository import TTbCartorioSaveRepository
from packages.v1.administrativo.schemas.t_tb_cartorio_schema import TTbCartorioSaveSchema
class TTbCartorioSaveAction(BaseAction):
    def execute(self, cartorio_schema: TTbCartorioSaveSchema):
        return TTbCartorioSaveRepository().execute(cartorio_schema)
