from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.c_caixa_servico_schema import CCaixaServicoSchema
from packages.v1.administrativo.repositories.c_caixa_servico.c_caixa_servico_show_repository import ShowRepository

class ShowAction(BaseAction):

    def execute(self, usuario_schema : CCaixaServicoSchema):

        # Instânciamento do repositório sql
        show_repository = ShowRepository()

        # Execução do sql
        response = show_repository.execute(usuario_schema)

        # Retorno da informação
        return response