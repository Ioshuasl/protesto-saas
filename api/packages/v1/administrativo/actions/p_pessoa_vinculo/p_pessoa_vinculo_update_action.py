from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_pessoa_vinculo.p_pessoa_vinculo_update_repository import (
    UpdateRepository,
)
from packages.v1.administrativo.schemas.p_pessoa_vinculo_schema import PPessoaVinculoUpdateSchema


class UpdateAction(BaseAction):
    def execute(self, pessoa_vinculo_id: int, vinculo_schema: PPessoaVinculoUpdateSchema):
        return UpdateRepository().execute(pessoa_vinculo_id, vinculo_schema)
