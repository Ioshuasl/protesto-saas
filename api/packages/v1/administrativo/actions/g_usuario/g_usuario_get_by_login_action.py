from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.g_usuario_schema import GUsuarioLoginSchema
from packages.v1.administrativo.repositories.g_usuario.g_usuario_get_by_login_repository import (
    GetByUsuarioLoginRepository,
)


class GetByUsuarioLoginAction(BaseAction):

    def execute(self, g_usuario_schema=GUsuarioLoginSchema):

        # Importação do repositório
        get_by_login_repository = GetByUsuarioLoginRepository()

        # Execução do repositório
        return get_by_login_repository.execute(g_usuario_schema)
