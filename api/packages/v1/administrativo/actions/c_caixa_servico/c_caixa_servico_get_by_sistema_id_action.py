from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.c_caixa_servico_schema import CCaixaServicoSistemaIdSchema
from packages.v1.administrativo.repositories.c_caixa_servico.c_caixa_servico_get_by_sistema_id_repository import ShowSistemaIdRepository

class ShowSistemaIdAction(BaseAction):

    def execute(self, caixa_servico_schema : CCaixaServicoSistemaIdSchema):

        # Instânciamento do repositório sql
        show_sistema_id_repository = ShowSistemaIdRepository()

        # Execução do sql
        response = show_sistema_id_repository.execute(caixa_servico_schema)

        # Retorno da informação
        return response