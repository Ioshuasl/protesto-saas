from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_especie.p_especie_delete_repository import (
    DeleteRepository,
)
from packages.v1.administrativo.schemas.p_especie_schema import PEspecieIdSchema


class DeleteAction(BaseAction):
    def execute(self, especie_schema: PEspecieIdSchema):
        return DeleteRepository().execute(especie_schema)
