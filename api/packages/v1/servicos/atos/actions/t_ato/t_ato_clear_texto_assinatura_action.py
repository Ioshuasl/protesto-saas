from abstracts.action import BaseAction

from packages.v1.servicos.atos.repositories.t_ato.t_ato_clear_texto_assinatura_repository import (
    TAtoClearTextoAssinaturaRepository,
)
from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoClearTextoAssinaturaSchema


class TAtoClearTextoAssinaturaAction(BaseAction):
    def execute(self, data: TAtoClearTextoAssinaturaSchema):
        return TAtoClearTextoAssinaturaRepository().execute(data)
