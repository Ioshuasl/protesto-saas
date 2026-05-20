from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.g_tb_documentotipo_schema import GTbDocumentoTipoIdSchema
from packages.v1.administrativo.repositories.g_tb_documentotipo.g_tb_documentotipo_delete_repository import DeleteRepository


class DeleteAction(BaseAction):

    def execute(self, documento_tipo_schema: GTbDocumentoTipoIdSchema):

        # Instanciamento do repositório
        delete_repository = DeleteRepository()

        # Execução do repositório
        return delete_repository.execute(documento_tipo_schema)