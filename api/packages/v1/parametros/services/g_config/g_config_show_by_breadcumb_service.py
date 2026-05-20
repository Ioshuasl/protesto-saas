from packages.v1.parametros.actions.g_config.g_config_show_by_breadcumb_action import (
    GConfigShowByBreadcumbAction,
)
from packages.v1.parametros.schemas.g_config_schema import (
    GConfigResponseSchema,
    GConfigShowByBreadcumbSchema,
)


class GConfigShowByBreadcumbService:

    def execute(self, data: GConfigShowByBreadcumbSchema) -> GConfigResponseSchema:

        # Instânciamento de Action
        action = GConfigShowByBreadcumbAction()

        # Execução da Ação
        return action.execute(data)
