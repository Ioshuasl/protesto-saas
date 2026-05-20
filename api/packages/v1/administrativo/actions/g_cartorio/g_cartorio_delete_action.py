from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_cartorio.g_cartorio_delete_repository import (
    GCartorioDeleteRepository,
)
from packages.v1.administrativo.schemas.g_cartorio_schema import GCartorioIdSchema


class GCartorioDeleteAction(BaseAction):

    def execute(self, g_cartorio_id_schema: GCartorioIdSchema):

        # Instanciamento do repositório
        g_cartorio_delete_repository = GCartorioDeleteRepository()

        # Execução da exclusão
        response = g_cartorio_delete_repository.execute(g_cartorio_id_schema)

        return response
