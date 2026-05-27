from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_titulo.p_titulo_devedores_repository import (
    DevedoresRepository,
)
from packages.v1.administrativo.schemas.p_titulo_schema import PTituloIdSchema


class DevedoresAction(BaseAction):
    def execute(self, titulo_schema: PTituloIdSchema) -> list[dict]:
        return DevedoresRepository().execute(titulo_schema)
