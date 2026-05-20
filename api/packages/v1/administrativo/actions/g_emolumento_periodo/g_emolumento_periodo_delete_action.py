from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_emolumento_periodo.g_emolumento_periodo_delete_repository import (
    GEmolumentoPeriodoDeleteRepository,
)
from packages.v1.administrativo.schemas.g_emolumento_periodo_schema import (
    GEmolumentoPeriodoIdSchema,
)


class GEmolumentoPeriodoDeleteAction(BaseAction):

    def execute(self, g_emolumento_periodo_id_schema: GEmolumentoPeriodoIdSchema):
        
        # Instanciamento do repositório        
        g_emolumento_periodo_delete_repository = GEmolumentoPeriodoDeleteRepository()
        
        # Execução da exclusão        
        response = g_emolumento_periodo_delete_repository.execute(
            g_emolumento_periodo_id_schema
        )

        return response
