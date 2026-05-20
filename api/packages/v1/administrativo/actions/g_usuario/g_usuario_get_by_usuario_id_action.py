from packages.v1.administrativo.schemas.g_usuario_schema import GUsuarioSchema
from packages.v1.administrativo.repositories.g_usuario.g_usuario_get_by_usuario_id_repository import GetByUsuarioIdRepository

class GetByUsuarioIdAction:

    def execute(self, g_usuario_schema = GUsuarioSchema):

        # Importação do repositório
        get_by_usuario_id_repository = GetByUsuarioIdRepository()

        # Execução do repositório
        return get_by_usuario_id_repository.execute(g_usuario_schema)
