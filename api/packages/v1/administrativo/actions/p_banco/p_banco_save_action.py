from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_banco.p_banco_save_repository import (
    SaveRepository,
)
from packages.v1.administrativo.schemas.p_banco_schema import PBancoSaveSchema


class SaveAction(BaseAction):
    def execute(self, banco_schema: PBancoSaveSchema):
        return SaveRepository().execute(banco_schema)
