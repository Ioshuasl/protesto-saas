from packages.v1.parametros.actions.g_config.g_config_show_by_nome_action import (
    GConfigShowByNomeAction,
)
from packages.v1.parametros.schemas.g_config_schema import (
    GConfigNomeSchema,
    GConfigResponseSchema,
)


class GConfigShowByNomeService:

    def execute(self, g_config_nome_schema: GConfigNomeSchema) -> GConfigResponseSchema:

        # Instânciamento de Action
        g_config_show_by_nome_action = GConfigShowByNomeAction()

        # Execução da Ação
        return g_config_show_by_nome_action.execute(g_config_nome_schema)
