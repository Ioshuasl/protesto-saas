from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_imovel_unidade.t_imovel_unidade_index_repository import (
    TImovelUnidadeIndexRepository,
)
from packages.v1.administrativo.schemas.t_imovel_unidade_schema import (
    TImovelUnidadeIndexSchema,
)


class TImovelUnidadeIndexAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de todos os registros na tabela t_censec_qualidade.
    """

    def execute(self, t_imovel_unidade_index_schema: TImovelUnidadeIndexSchema):
        """
        Executa a operação de listagem no banco de dados.

        Returns:
            A lista de todos os registros.
        """
        # Instanciamento do repositório
        index_repository = TImovelUnidadeIndexRepository()

        # Execução do repositório
        response = index_repository.execute(t_imovel_unidade_index_schema)

        # Retorno da informação
        return response
