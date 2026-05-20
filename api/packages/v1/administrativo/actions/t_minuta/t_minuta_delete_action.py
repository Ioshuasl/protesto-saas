from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.t_minuta_schema import TMinutaIdSchema
from packages.v1.administrativo.repositories.t_minuta.t_minuta_delete_repository import DeleteRepository


class DeleteAction(BaseAction):
    
    def execute(self, minuta_schema: TMinutaIdSchema):

        # Instanciamento do repositório
        delete_repository = DeleteRepository()

        # Execução do repositório
        return delete_repository.execute(minuta_schema)