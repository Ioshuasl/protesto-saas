from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.c_caixa_servico_schema import CCaixaServicoDescricaoSchema
from packages.v1.administrativo.repositories.c_caixa_servico.c_caixa_servico_get_by_descricao_repository import ShowRepository

class ShowAction(BaseAction):

    def execute(self, caixa_servico_schema : CCaixaServicoDescricaoSchema):

        # Instânciamento do repositório sql
        show_repository = ShowRepository()

        # Execução do sql
        response = show_repository.execute(caixa_servico_schema)

        # Retorno da informação
        return response