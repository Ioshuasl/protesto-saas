from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_titulo.p_titulo_update_repository import (
    UpdateRepository,
)
from packages.v1.administrativo.schemas.p_titulo_schema import PTituloUpdateSchema


class UpdateAction(BaseAction):
    def execute(self, titulo_id: int, titulo_schema: PTituloUpdateSchema):
        return UpdateRepository().execute(titulo_id, titulo_schema)
