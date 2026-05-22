from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_pessoa.p_pessoa_save_repository import (
    SaveRepository,
)
from packages.v1.administrativo.schemas.p_pessoa_schema import PPessoaSaveSchema


class SaveAction(BaseAction):
    def execute(self, pessoa_schema: PPessoaSaveSchema):
        return SaveRepository().execute(pessoa_schema)
