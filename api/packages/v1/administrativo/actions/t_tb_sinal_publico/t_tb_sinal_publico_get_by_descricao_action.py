from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_tb_sinal_publico.t_tb_sinal_publico_get_by_descricao_repository import (
    TTbSinalPublicoGetByDescricaoRepository,
)
from packages.v1.administrativo.schemas.t_tb_sinal_publico_schema import (
    TTbSinalPublicoDescricaoSchema,
)


class TTbSinalPublicoGetByDescricaoAction(BaseAction):
    def execute(self, sinal_publico_schema: TTbSinalPublicoDescricaoSchema):
        repository = TTbSinalPublicoGetByDescricaoRepository()
        return repository.execute(sinal_publico_schema)
