from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_tb_sinal_publico.t_tb_sinal_publico_save_repository import (
    TTbSinalPublicoSaveRepository,
)
from packages.v1.administrativo.schemas.t_tb_sinal_publico_schema import (
    TTbSinalPublicoSaveSchema,
)


class TTbSinalPublicoSaveAction(BaseAction):
    def execute(self, sinal_publico_schema: TTbSinalPublicoSaveSchema):
        save_repository = TTbSinalPublicoSaveRepository()
        return save_repository.execute(sinal_publico_schema)
