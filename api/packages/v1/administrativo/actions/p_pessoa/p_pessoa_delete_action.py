from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_pessoa.p_pessoa_delete_repository import (
    DeleteRepository,
)
from packages.v1.administrativo.schemas.p_pessoa_schema import PPessoaIdSchema


class DeleteAction(BaseAction):
    def execute(self, pessoa_schema: PPessoaIdSchema):
        return DeleteRepository().execute(pessoa_schema)
