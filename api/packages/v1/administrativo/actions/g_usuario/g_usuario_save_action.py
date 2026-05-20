from packages.v1.administrativo.schemas.g_usuario_schema import GUsuarioSaveSchema
from packages.v1.administrativo.repositories.g_usuario.g_usuario_save_repository import SaveRepository


class SaveAction:

    def execute(self, usuario_schema : GUsuarioSaveSchema):

        save_repository = SaveRepository()

        return save_repository.execute(usuario_schema)