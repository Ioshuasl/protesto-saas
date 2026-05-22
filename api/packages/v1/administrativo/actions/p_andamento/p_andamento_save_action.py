from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_andamento.p_andamento_save_repository import (
    SaveRepository,
)
from packages.v1.administrativo.schemas.p_andamento_schema import PAndamentoSaveSchema


class SaveAction(BaseAction):
    def execute(self, andamento_schema: PAndamentoSaveSchema):
        return SaveRepository().execute(andamento_schema)
