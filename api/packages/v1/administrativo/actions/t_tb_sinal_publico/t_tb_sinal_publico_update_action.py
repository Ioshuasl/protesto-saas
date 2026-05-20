from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_tb_sinal_publico.t_tb_sinal_publico_update_repository import (
    TTbSinalPublicoUpdateRepository,
)
from packages.v1.administrativo.schemas.t_tb_sinal_publico_schema import (
    TTbSinalPublicoUpdateSchema,
)


class TTbSinalPublicoUpdateAction(BaseAction):
    def execute(
        self,
        tb_sinalpublico_id: int,
        sinal_publico_schema: TTbSinalPublicoUpdateSchema,
    ):
        update_repository = TTbSinalPublicoUpdateRepository()
        return update_repository.execute(tb_sinalpublico_id, sinal_publico_schema)
