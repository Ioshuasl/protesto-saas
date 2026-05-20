from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_natureza_titulo.g_natureza_titulo_delete_repository import (
    GNaturezaTituloDeleteRepository,
)
from packages.v1.administrativo.schemas.g_natureza_titulo_schema import (
    GNaturezaTituloIdSchema,
)


class GNaturezaTituloDeleteAction(BaseAction):

    def execute(self, g_natureza_titulo_id_schema: GNaturezaTituloIdSchema):
        
        # Instanciamento do repositório        
        g_natureza_titulo_delete_repository = GNaturezaTituloDeleteRepository()
        
        # Execução da exclusão        
        response = g_natureza_titulo_delete_repository.execute(
            g_natureza_titulo_id_schema
        )

        return response
