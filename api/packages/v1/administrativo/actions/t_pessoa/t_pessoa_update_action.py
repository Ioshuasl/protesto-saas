from packages.v1.administrativo.repositories.t_pessoa.t_pessoa_update_repository import (
    TPessoaUpdateRepository,
)
from packages.v1.administrativo.schemas.t_pessoa_schema import TPessoaUpdateSchema


class TPessoaUpdateAction:
    """
    Service responsável por encapsular a lógica de negócio para a atualização
    de um registro na tabela g_tb_regimebens.
    """

    def execute(self, t_pessoa_update_schema: TPessoaUpdateSchema):
        """
        Executa a operação de atualização.

        Args:
        regimebens_schema (GTbRegimebensUpdateSchema): O esquema com os dados a serem atualizados.

            Returns:
                O resultado da operação de atualização.
        """
        # Instância o repositório de atualização
        t_pessoa_update_repository = TPessoaUpdateRepository()

        # Chama o método de execução do repositório para realizar a atualização
        return t_pessoa_update_repository.execute(t_pessoa_update_schema)
