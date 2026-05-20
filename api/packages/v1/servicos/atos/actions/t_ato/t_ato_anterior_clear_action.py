from abstracts.action import BaseAction

from packages.v1.servicos.atos.repositories.t_ato.t_ato_anterior_clear_repository import (
    TAtoAnteriorClearRepository,
)
from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoAnteriorClearSchema


class TAtoAnteriorClearAction(BaseAction):
    def execute(self, data: TAtoAnteriorClearSchema):
        return TAtoAnteriorClearRepository().execute(data)
