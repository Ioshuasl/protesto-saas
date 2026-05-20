from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_censec_tipoato.t_censec_tipoato_delete_repository import (
    TCensecTipoAtoDeleteRepository,
)
from packages.v1.administrativo.schemas.t_censec_tipoato_schema import (
    TCensecTipoAtoIdSchema,
)


class TCensecTipoAtoDeleteAction(BaseAction):
    
    def execute(self, t_censec_tipoato_id_schema: TCensecTipoAtoIdSchema):
        
        
        # Instanciamento do repositório        
        t_censec_tipoato_delete_repository = TCensecTipoAtoDeleteRepository()
        
        # Execução da exclusão        
        response = t_censec_tipoato_delete_repository.execute(
            t_censec_tipoato_id_schema
        )

        return response
