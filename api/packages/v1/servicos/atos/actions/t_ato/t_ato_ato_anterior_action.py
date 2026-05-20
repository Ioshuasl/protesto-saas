from packages.v1.servicos.atos.repositories.t_ato.t_ato_ato_anterior_repository import (
    TAtoAtoAnteriorRepository,
)
from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoIdSchema


class TAtoAtoAnteriorAction:
    def execute(self, t_ato_id_schema: TAtoIdSchema):
        return TAtoAtoAnteriorRepository().execute(t_ato_id_schema)
