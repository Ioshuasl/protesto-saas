from abstracts.action import BaseAction

from packages.v1.servicos.atos.repositories.t_ato.t_ato_anterior_update_repository import (
    TAtoAnteriorUpdateRepository,
)
from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoAnteriorUpdateSchema


class TAtoAnteriorUpdateAction(BaseAction):
    def execute(self, t_ato_anterior_update_schema: TAtoAnteriorUpdateSchema):
        return TAtoAnteriorUpdateRepository().execute(t_ato_anterior_update_schema)
