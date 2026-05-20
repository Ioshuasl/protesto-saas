from packages.v1.parametros.repositories.g_config.g_config_show_by_breadcumb_repository import (
    GConfigShowByBreadcumbRepository,
)

from packages.v1.parametros.schemas.g_config_schema import (
    GConfigResponseSchema,
    GConfigShowByBreadcumbSchema,
)
from abstracts.action import BaseAction


class GConfigShowByBreadcumbAction(BaseAction):

    def execute(self, data: GConfigShowByBreadcumbSchema) -> GConfigResponseSchema:

        # Instânciamento de repositório
        repository = GConfigShowByBreadcumbRepository()

        # Execução do repositório
        return repository.execute(data)
