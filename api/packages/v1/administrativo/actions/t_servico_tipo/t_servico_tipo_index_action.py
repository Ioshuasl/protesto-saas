from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_servico_tipo.t_servico_tipo_index_repository import (
    IndexRepository,
)
from packages.v1.administrativo.schemas.t_servico_tipo_schema import (
    TServicoTipoIndexSchema,
)


class IndexAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de todos os registros na tabela T_SERVICO_TIPO.
    """

    def execute(self, t_servico_tipo_index_schema: TServicoTipoIndexSchema):
        """
        Executa a operação de listagem no banco de dados.

        Returns:
            A lista de todos os registros.
        """
        # Instanciamento do repositório
        index_repository = IndexRepository()

        # Execução do repositório
        response = index_repository.execute(t_servico_tipo_index_schema)

        # Retorno da informação
        return response
