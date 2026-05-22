from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_andamento.p_andamento_delete_repository import (
    DeleteRepository,
)
from packages.v1.administrativo.schemas.p_andamento_schema import PAndamentoIdSchema


class DeleteAction(BaseAction):
    def execute(self, andamento_schema: PAndamentoIdSchema):
        return DeleteRepository().execute(andamento_schema)
