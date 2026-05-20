from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.t_tb_reconhecimentotipo_schema import TTbReconhecimentotipoIdSchema
from packages.v1.administrativo.repositories.t_tb_reconhecimentotipo.t_tb_reconhecimentotipo_delete_repository import DeleteRepository


class DeleteAction(BaseAction):

    def execute(self, reconhecimentotipo_schema: TTbReconhecimentotipoIdSchema):

        # Instanciamento do repositório
        delete_repository = DeleteRepository()

        # Execução do repositório
        return delete_repository.execute(reconhecimentotipo_schema)
