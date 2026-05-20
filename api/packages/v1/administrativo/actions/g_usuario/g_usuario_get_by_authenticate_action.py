from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.g_usuario_schema import (
    GUsuarioAuthenticateSchema,
)
from packages.v1.administrativo.repositories.g_usuario.g_usuario_get_by_authenticate_repository import (
    GetByAuthenticateRepository,
)


class GetByAuthenticateAction(BaseAction):

    def execute(self, g_usuario_authenticate_schema: GUsuarioAuthenticateSchema):

        # Instânciamento do repositório de busca pelo authenticate
        get_by_authenticate_repository = GetByAuthenticateRepository()

        # Execução do repositório
        return get_by_authenticate_repository.execute(g_usuario_authenticate_schema)
