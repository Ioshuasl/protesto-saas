from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_titulo.p_titulo_delete_repository import (
    DeleteRepository,
)
from packages.v1.administrativo.schemas.p_titulo_schema import PTituloIdSchema


class DeleteAction(BaseAction):
    def execute(self, titulo_schema: PTituloIdSchema):
        return DeleteRepository().execute(titulo_schema)
