from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_titulo.p_titulo_save_repository import (
    SaveRepository,
)
from packages.v1.administrativo.schemas.p_titulo_schema import PTituloSaveSchema


class SaveAction(BaseAction):
    def execute(self, titulo_schema: PTituloSaveSchema):
        return SaveRepository().execute(titulo_schema)
