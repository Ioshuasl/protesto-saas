from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_pessoa.t_pessoa_delete_repository import (
    TPessoaDeleteRepository,
)
from packages.v1.administrativo.schemas.t_pessoa_schema import TPessoaIdSchema


class TPessoaDeleteAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de exclusão de um registro na tabela g_tb_regimebens.
    """

    def execute(self, t_pessoa_id_schema: TPessoaIdSchema):
        """
        Executa a operação de exclusão no banco de dados.

        Args:
            regimebens_schema (GTbRegimebensIdSchema): O esquema com o ID a ser excluído.

        Returns:
            O resultado da operação de exclusão.
        """
        # Instanciamento do repositório
        t_pessoa_delete_repository = TPessoaDeleteRepository()

        # Execução do repositório
        return t_pessoa_delete_repository.execute(t_pessoa_id_schema)
