from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_selo_grupo.g_selo_grupo_delete_repository import (
    GSeloGrupoDeleteRepository,
)
from packages.v1.administrativo.schemas.g_selo_grupo_schema import GSeloGrupoIdSchema


class GSeloGrupoDeleteAction(BaseAction):

    def execute(self, g_selo_grupo_id_schema: GSeloGrupoIdSchema):
        
        # Instanciamento do repositório        
        g_selo_grupo_delete_repository = GSeloGrupoDeleteRepository()
        
        # Execução da exclusão        
        response = g_selo_grupo_delete_repository.execute(g_selo_grupo_id_schema)

        return response
