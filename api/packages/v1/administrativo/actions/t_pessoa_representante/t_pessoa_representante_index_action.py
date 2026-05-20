from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_pessoa_representante.t_pessoa_representante_index_repository import (
    TPessoaRepresentanteIndexRepository,
)
from packages.v1.administrativo.schemas.t_pessoa_representante_schema import (
    TPessoaRepresentantePessoaIdSchema,
)


class TPessoaRepresentanteIndexAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de todos os registros na tabela g_tb_regimebens.
    """

    def execute(
        self,
        t_pessoa_representante_pessoa_id_schema: TPessoaRepresentantePessoaIdSchema,
    ):
        """
        Executa a operação de listagem no banco de dados.

        Returns:
            A lista de todos os registros.
        """
        # Instanciamento do repositório
        t_pessoa_representante_index_repository = TPessoaRepresentanteIndexRepository()

        # Execução do repositório
        response = t_pessoa_representante_index_repository.execute(
            t_pessoa_representante_pessoa_id_schema
        )

        # Retorno da informação
        return response
