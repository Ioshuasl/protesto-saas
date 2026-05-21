from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_especie.p_especie_show_repository import (
    ShowRepository,
)
from packages.v1.administrativo.schemas.p_especie_schema import PEspecieIdSchema


class ShowAction(BaseAction):
    def execute(self, especie_schema: PEspecieIdSchema):
        return ShowRepository().execute(especie_schema)
