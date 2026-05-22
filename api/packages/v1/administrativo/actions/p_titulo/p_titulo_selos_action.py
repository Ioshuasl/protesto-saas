from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_titulo.p_titulo_selos_repository import (
    SelosRepository,
)
from packages.v1.administrativo.schemas.p_titulo_schema import PTituloIdSchema


class SelosAction(BaseAction):
    def execute(self, titulo_schema: PTituloIdSchema) -> list[dict]:
        return SelosRepository().execute(titulo_schema)
