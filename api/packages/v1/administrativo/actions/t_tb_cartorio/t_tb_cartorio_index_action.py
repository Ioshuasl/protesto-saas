from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_tb_cartorio.t_tb_cartorio_index_repository import TTbCartorioIndexRepository
class TTbCartorioIndexAction(BaseAction):
    def execute(self):
        return TTbCartorioIndexRepository().execute()
