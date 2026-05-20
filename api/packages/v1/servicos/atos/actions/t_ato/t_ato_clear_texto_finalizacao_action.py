from abstracts.action import BaseAction

from packages.v1.servicos.atos.repositories.t_ato.t_ato_clear_texto_finalizacao_repository import (
    TAtoClearTextoFinalizacaoRepository,
)
from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoClearTextoFinalizacaoSchema


class TAtoClearTextoFinalizacaoAction(BaseAction):
    def execute(self, data: TAtoClearTextoFinalizacaoSchema):
        return TAtoClearTextoFinalizacaoRepository().execute(data)
