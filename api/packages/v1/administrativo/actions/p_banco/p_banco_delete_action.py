from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_banco.p_banco_delete_repository import (
    DeleteRepository,
)
from packages.v1.administrativo.schemas.p_banco_schema import PBancoIdSchema


class DeleteAction(BaseAction):
    def execute(self, banco_schema: PBancoIdSchema):
        return DeleteRepository().execute(banco_schema)
