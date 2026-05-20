from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_tb_sinal_publico.t_tb_sinal_publico_delete_repository import (
    TTbSinalPublicoDeleteRepository,
)
from packages.v1.administrativo.schemas.t_tb_sinal_publico_schema import (
    TTbSinalPublicoIdSchema,
)


class TTbSinalPublicoDeleteAction(BaseAction):
    def execute(self, sinal_publico_schema: TTbSinalPublicoIdSchema):
        delete_repository = TTbSinalPublicoDeleteRepository()
        return delete_repository.execute(sinal_publico_schema)
