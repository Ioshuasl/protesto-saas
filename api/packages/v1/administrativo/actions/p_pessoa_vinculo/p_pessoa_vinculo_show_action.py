from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_pessoa_vinculo.p_pessoa_vinculo_show_repository import (
    ShowRepository,
)
from packages.v1.administrativo.schemas.p_pessoa_vinculo_schema import PPessoaVinculoIdSchema


class ShowAction(BaseAction):
    def execute(self, vinculo_schema: PPessoaVinculoIdSchema):
        return ShowRepository().execute(vinculo_schema)
