from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_certidao.p_certidao_save_repository import (
    SaveRepository,
)
from packages.v1.administrativo.schemas.p_certidao_schema import PCertidaoSaveSchema


class SaveAction(BaseAction):
    def execute(self, certidao_schema: PCertidaoSaveSchema):
        return SaveRepository().execute(certidao_schema)
