from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_censec_tiponatureza.t_censec_tiponatureza_delete_repository import (
    TCensecTipoNaturezaDeleteRepository,
)
from packages.v1.administrativo.schemas.t_censec_tiponatureza_schema import (
    TCensecTipoNaturezaIdSchema,
)


class TCensecTipoNaturezaDeleteAction(BaseAction):
    
    def execute(self, t_censec_tiponatureza_id_schema: TCensecTipoNaturezaIdSchema):
                
        # Instanciamento do repositório        
        t_censec_tiponatureza_delete_repository = TCensecTipoNaturezaDeleteRepository()
        
        # Execução da exclusão        
        response = t_censec_tiponatureza_delete_repository.execute(
            t_censec_tiponatureza_id_schema
        )

        return response
