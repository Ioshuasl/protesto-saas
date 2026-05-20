from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_tb_sinal_publico.t_tb_sinal_publico_show_repository import (
    TTbSinalPublicoShowRepository,
)
from packages.v1.administrativo.schemas.t_tb_sinal_publico_schema import (
    TTbSinalPublicoIdSchema,
)


class TTbSinalPublicoShowAction(BaseAction):
    def execute(self, sinal_publico_schema: TTbSinalPublicoIdSchema):
        show_repository = TTbSinalPublicoShowRepository()
        return show_repository.execute(sinal_publico_schema)
