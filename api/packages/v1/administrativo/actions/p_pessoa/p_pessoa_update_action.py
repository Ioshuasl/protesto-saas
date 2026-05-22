from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_pessoa.p_pessoa_update_repository import (
    UpdateRepository,
)
from packages.v1.administrativo.schemas.p_pessoa_schema import PPessoaUpdateSchema


class UpdateAction(BaseAction):
    def execute(self, pessoa_id: int, pessoa_schema: PPessoaUpdateSchema):
        return UpdateRepository().execute(pessoa_id, pessoa_schema)
