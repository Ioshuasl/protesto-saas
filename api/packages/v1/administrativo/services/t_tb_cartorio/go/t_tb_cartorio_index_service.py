from packages.v1.administrativo.actions.t_tb_cartorio.t_tb_cartorio_index_action import TTbCartorioIndexAction
class TTbCartorioIndexService:
    def execute(self):
        return TTbCartorioIndexAction().execute()
