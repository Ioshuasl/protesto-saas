from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.g_usuario_schema import GUsuarioSchema
from packages.v1.administrativo.repositories.g_usuario.g_usuario_show_repository import ShowRepository

class ShowAction(BaseAction):

    def execute(self, usuario_schema : GUsuarioSchema):

        # Instânciamento do repositório sql
        show_repository = ShowRepository()

        # Execução do sql
        response = show_repository.execute(usuario_schema)

        # Retorno da informação
        return response