from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_tb_sinal_publico.t_tb_sinal_publico_index_repository import (
    TTbSinalPublicoIndexRepository,
)


class TTbSinalPublicoIndexAction(BaseAction):
    def execute(self):
        index_repository = TTbSinalPublicoIndexRepository()
        return index_repository.execute()
