from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.t_servico_tipo_schema import TServicoTipoIdSchema
from packages.v1.administrativo.repositories.t_servico_tipo.t_servico_tipo_delete_repository import DeleteRepository


class DeleteAction(BaseAction):

    def execute(self, servico_tipo_schema: TServicoTipoIdSchema):

        # Instanciamento do repositório
        delete_repository = DeleteRepository()

        # Execução do repositório
        return delete_repository.execute(servico_tipo_schema)