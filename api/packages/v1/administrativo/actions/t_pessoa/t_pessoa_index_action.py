from packages.v1.administrativo.repositories.t_pessoa.t_pessoa_index_repository import (
    TPessoaIndexRepository,
)
from packages.v1.administrativo.schemas.t_pessoa_schema import TPessoaTipoSchema


class TPessoaIndexAction:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de todos os registros na tabela g_tb_regimebens.
    """

    def execute(self, t_pessoa_tipo_schema: TPessoaTipoSchema):
        """
        Executa a operação de listagem no banco de dados.

        Returns:
            A lista de todos os registros.
        """
        # Instanciamento do repositório
        t_pessoa_index_repository = TPessoaIndexRepository()

        # Execução do repositório
        response = t_pessoa_index_repository.execute(t_pessoa_tipo_schema)

        # Retorno da informação
        return response
