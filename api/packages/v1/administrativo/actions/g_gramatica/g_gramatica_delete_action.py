from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_gramatica.g_gramatica_delete_repository import (
    GGramaticaDeleteRepository,
)
from packages.v1.administrativo.schemas.g_gramatica_schema import GGramaticaIdSchema


class GGramaticaDeleteAction(BaseAction):

    def execute(self, g_gramatica_id_schema: GGramaticaIdSchema):
        
        # Instanciamento do repositório        
        g_gramatica_delete_repository = GGramaticaDeleteRepository()
        
        # Execução da exclusão        
        response = g_gramatica_delete_repository.execute(g_gramatica_id_schema)

        return response
