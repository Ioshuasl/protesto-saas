from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.t_servico_etiqueta_schema import (
    TServicoEtiquetaIdSchema,
)
from packages.v1.administrativo.repositories.t_servico_etiqueta.t_servico_etiqueta_delete_repository import (
    DeleteRepository,
)


class DeleteAction(BaseAction):

    def execute(self, servico_etiqueta_schema: TServicoEtiquetaIdSchema):

        # Instanciamento do repositório
        delete_repository = DeleteRepository()

        # Execução do repositório
        return delete_repository.execute(servico_etiqueta_schema)
