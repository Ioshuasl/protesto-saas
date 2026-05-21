from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_especie.p_especie_save_repository import (
    SaveRepository,
)
from packages.v1.administrativo.schemas.p_especie_schema import PEspecieSaveSchema


class SaveAction(BaseAction):
    def execute(self, especie_schema: PEspecieSaveSchema):
        return SaveRepository().execute(especie_schema)
