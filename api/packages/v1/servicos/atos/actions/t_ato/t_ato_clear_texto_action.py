from abstracts.action import BaseAction

from packages.v1.servicos.atos.repositories.t_ato.t_ato_clear_texto_repository import (
    TAtoClearTextoRepository,
)
from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoClearTextoSchema


class TAtoClearTextoAction(BaseAction):
    def execute(self, data: TAtoClearTextoSchema):
        return TAtoClearTextoRepository().execute(data)
