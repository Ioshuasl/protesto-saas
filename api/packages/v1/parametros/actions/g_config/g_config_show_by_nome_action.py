from packages.v1.parametros.repositories.g_config.g_config_show_by_nome_repository import (
    GConfigShowByNomeRepository,
)
from packages.v1.parametros.schemas.g_config_schema import (
    GConfigNomeSchema,
    GConfigResponseSchema,
)
from abstracts.action import BaseAction


class GConfigShowByNomeAction(BaseAction):

    def execute(self, g_config_nome_schema: GConfigNomeSchema) -> GConfigResponseSchema:

        # Instânciamento de repositório
        g_config_show_by_nome_repository = GConfigShowByNomeRepository()

        # Execução do repositório
        return g_config_show_by_nome_repository.execute(g_config_nome_schema)
