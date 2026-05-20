from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.t_censec_qualidade_schema import TCensecQualidadeIdSchema
from packages.v1.administrativo.repositories.t_censec_qualidade.t_censec_qualidade_delete_repository import DeleteRepository


class DeleteAction(BaseAction):
    
    def execute(self, censec_qualidade_schema: TCensecQualidadeIdSchema):
        
        # Instanciamento do repositório
        delete_repository = DeleteRepository()

        # Execução do repositório
        return delete_repository.execute(censec_qualidade_schema)