from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_pessoa_vinculo.p_pessoa_vinculo_delete_repository import (
    DeleteRepository,
)
from packages.v1.administrativo.schemas.p_pessoa_vinculo_schema import PPessoaVinculoIdSchema


class DeleteAction(BaseAction):
    def execute(self, vinculo_schema: PPessoaVinculoIdSchema) -> bool:
        return DeleteRepository().execute(vinculo_schema)
