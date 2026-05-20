from packages.v1.administrativo.schemas.g_usuario_schema import GUsuarioUpdateSchema
from packages.v1.administrativo.repositories.g_usuario.g_usuario_update_repository import UpdateRepository


class UpdateAction:

    def execute(self, usuario_id: int, usuario_schema : GUsuarioUpdateSchema):

        save_repository = UpdateRepository()

        return save_repository.execute(usuario_id, usuario_schema)