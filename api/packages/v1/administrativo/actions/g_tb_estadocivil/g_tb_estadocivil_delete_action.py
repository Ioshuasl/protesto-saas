from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.g_tb_estadocivil_schema import GTbEstadoCivilIdSchema
from packages.v1.administrativo.repositories.g_tb_estadocivil.g_tb_estadocivil_delete_repository import DeleteRepository


class DeleteAction(BaseAction):

    def execute(self, estadocivil_schema: GTbEstadoCivilIdSchema):

        # Instanciamento do repositório
        delete_repository = DeleteRepository()

        # Execução do repositório
        return delete_repository.execute(estadocivil_schema)