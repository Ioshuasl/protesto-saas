from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_pessoa.p_pessoa_show_repository import (
    ShowRepository,
)
from packages.v1.administrativo.schemas.p_pessoa_schema import PPessoaIdSchema


class ShowAction(BaseAction):
    def execute(self, pessoa_schema: PPessoaIdSchema):
        return ShowRepository().execute(pessoa_schema.pessoa_id)
