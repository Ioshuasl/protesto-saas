from packages.v1.administrativo.schemas.g_usuario_schema import GUsuarioIdSchema
from packages.v1.administrativo.repositories.g_usuario.g_usuario_delete_repository import (
    DeleteRepository,
)


class DeleteAction:

    def execute(self, usuario_schema: GUsuarioIdSchema):

        delete_repository = DeleteRepository()

        return delete_repository.execute(usuario_schema)
