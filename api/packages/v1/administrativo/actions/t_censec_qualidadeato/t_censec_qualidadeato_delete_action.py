from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_censec_qualidadeato.t_censec_qualidadeato_delete_repository import (
    TCensecQualidadeAtoDeleteRepository,
)
from packages.v1.administrativo.schemas.t_censec_qualidadeato_schema import (
    TCensecQualidadeAtoIdSchema,
)


class TCensecQualidadeAtoDeleteAction(BaseAction):
    
    def execute(self, t_censec_qualidadeato_id_schema: TCensecQualidadeAtoIdSchema):        
        
        # Instanciamento do repositório        
        t_censec_qualidadeato_delete_repository = TCensecQualidadeAtoDeleteRepository()
        
        # Execução da exclusão        
        response = t_censec_qualidadeato_delete_repository.execute(
            t_censec_qualidadeato_id_schema
        )
        
        # Retorno do resultado        
        return response
