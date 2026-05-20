from packages.v1.administrativo.schemas.c_caixa_servico_schema import CCaixaServicoIdSchema
from packages.v1.administrativo.repositories.c_caixa_servico.c_caixa_servico_delete_repository import DeleteRepository


class DeleteAction:

    def execute(self, usuario_schema : CCaixaServicoIdSchema):

        delete_repository = DeleteRepository()

        return delete_repository.execute(usuario_schema)