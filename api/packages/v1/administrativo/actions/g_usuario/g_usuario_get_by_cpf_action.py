from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.g_usuario_schema import GUsuarioCpfSchema
from packages.v1.administrativo.repositories.g_usuario.g_usuario_get_by_cpf_repository import GetByUsuarioCpfRepository

class GetByUsuarioCpfAction(BaseAction):

    def execute(self, g_usuario_schema = GUsuarioCpfSchema):

        # Importação do repositório
        get_by_cpf_repository = GetByUsuarioCpfRepository()

        # Execução do repositório
        return get_by_cpf_repository.execute(g_usuario_schema)
