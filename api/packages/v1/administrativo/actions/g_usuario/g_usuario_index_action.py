from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_usuario.g_usuario_index_repository import (
    IndexRepository,
)
from packages.v1.administrativo.schemas.g_usuario_schema import GUsuarioIndexSchema


class IndexAction(BaseAction):

    def execute(self, g_usuario_index_schema: GUsuarioIndexSchema):

        # Instânciamento do repositório sql
        index_repository = IndexRepository()

        # Execução do sql
        response = index_repository.execute(g_usuario_index_schema)

        # Retorno da informação
        return response
