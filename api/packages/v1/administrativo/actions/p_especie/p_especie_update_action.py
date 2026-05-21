from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_especie.p_especie_update_repository import (
    UpdateRepository,
)
from packages.v1.administrativo.schemas.p_especie_schema import PEspecieUpdateSchema


class UpdateAction(BaseAction):
    def execute(self, especie_id: int, especie_schema: PEspecieUpdateSchema):
        return UpdateRepository().execute(especie_id, especie_schema)
