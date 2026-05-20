from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.g_usuario_schema import GUsuarioEmailSchema
from packages.v1.administrativo.repositories.g_usuario.g_usuario_get_by_email_repository import GetByUsuarioEmailRepository

class GetByUsuarioEmailAction(BaseAction):

    def execute(self, g_usuario_schema = GUsuarioEmailSchema):

        # Importação do repositório
        get_by_email_repository = GetByUsuarioEmailRepository()

        # Execução do repositório
        return get_by_email_repository.execute(g_usuario_schema)
