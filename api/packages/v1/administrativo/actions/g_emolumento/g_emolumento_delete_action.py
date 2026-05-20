from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_emolumento.g_emolumento_delete_repository import (
    GEmolumentoDeleteRepository,
)
from packages.v1.administrativo.schemas.g_emolumento_schema import GEmolumentoIdSchema


class GEmolumentoDeleteAction(BaseAction):

    def execute(self, g_emolumento_id_schema: GEmolumentoIdSchema):

        # Instanciamento do repositório
        g_emolumento_delete_repository = GEmolumentoDeleteRepository()

        # Execução da exclusão
        response = g_emolumento_delete_repository.execute(g_emolumento_id_schema)

        return response
