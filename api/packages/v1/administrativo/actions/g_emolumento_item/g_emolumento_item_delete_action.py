from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_emolumento_item.g_emolumento_item_delete_repository import (
    GEmolumentoItemDeleteRepository,
)
from packages.v1.administrativo.schemas.g_emolumento_item_schema import (
    GEmolumentoItemIdSchema,
)


class GEmolumentoItemDeleteAction(BaseAction):

    def execute(self, g_emolumento_item_id_schema: GEmolumentoItemIdSchema):
        
        # Instanciamento do repositório        
        g_emolumento_item_delete_repository = GEmolumentoItemDeleteRepository()
        
        # Execução da exclusão        
        response = g_emolumento_item_delete_repository.execute(
            g_emolumento_item_id_schema
        )

        return response
