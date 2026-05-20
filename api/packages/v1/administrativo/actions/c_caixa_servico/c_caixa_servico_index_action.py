from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.c_caixa_servico.c_caixa_servico_index_repository import (
    IndexRepository,
)


class IndexAction(BaseAction):

    def execute(self):

        # Instânciamento do repositório sql
        index_repository = IndexRepository()

        # Execução do sql
        response = index_repository.execute()

        # Retorno da informação
        return response
