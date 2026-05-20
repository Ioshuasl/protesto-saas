from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.t_censec_schema import TCensecIdSchema
from packages.v1.administrativo.repositories.t_censec.t_censec_delete_repository import DeleteRepository


class DeleteAction(BaseAction):

    def execute(self, censec_schema: TCensecIdSchema):
        
        # Instanciamento do repositório
        delete_repository = DeleteRepository()

        # Execução do repositório
        return delete_repository.execute(censec_schema)