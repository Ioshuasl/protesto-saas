from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_pessoa_vinculo.p_pessoa_vinculo_save_repository import (
    SaveRepository,
)
from packages.v1.administrativo.schemas.p_pessoa_vinculo_schema import PPessoaVinculoSaveSchema


class SaveAction(BaseAction):
    def execute(self, vinculo_schema: PPessoaVinculoSaveSchema):
        return SaveRepository().execute(vinculo_schema)
