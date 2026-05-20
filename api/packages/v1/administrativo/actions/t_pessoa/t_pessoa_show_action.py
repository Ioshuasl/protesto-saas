from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_pessoa.t_pessoa_show_repository import (
    TPessoaShowRepository,
)
from packages.v1.administrativo.schemas.t_pessoa_schema import TPessoaIdSchema


class TPessoaShowAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a exibição
    de um registro na tabela g_tb_regimebens.
    """

    def execute(self, t_pessoa_id_schema: TPessoaIdSchema):
        """
        Executa a operação de exibição.

        Args:
            regimebens_schema (GTbRegimebensIdSchema): O esquema com o ID do registro a ser exibido.

        Returns:
            O resultado da operação de exibição.
        """
        # Instânciamento do repositório
        t_pessoa_show_repository = TPessoaShowRepository()

        # Execução do repositório
        response = t_pessoa_show_repository.execute(t_pessoa_id_schema)

        # Retorno da informação
        return response
