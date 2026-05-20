from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.g_medida_tipo_schema import GMedidaTipoIdSchema
from packages.v1.administrativo.repositories.g_medida_tipo.g_medida_tipo_delete_repository import DeleteRepository


class DeleteAction(BaseAction):

    def execute(self, medida_tipo_schema: GMedidaTipoIdSchema):

        # Instanciamento do repositório
        delete_repository = DeleteRepository()

        # Execução do repositório
        return delete_repository.execute(medida_tipo_schema)