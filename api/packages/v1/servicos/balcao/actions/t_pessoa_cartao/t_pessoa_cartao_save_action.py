from abstracts.action import BaseAction
from packages.v1.servicos.balcao.repositories.t_pessoa_cartao.t_pessoa_cartao_save_repository import (
    TPessoaCartaoSaveRepository,
)
from packages.v1.servicos.balcao.schemas.t_pessoa_cartao_schema import (
    TPessoaCartaoSaveSchema,
)


class TPessoaCartaoSaveAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de salvamento de um novo registro na tabela T_PESSOA_CARTAO.
    """

    def execute(self, t_pessoa_cartao_save_schema: TPessoaCartaoSaveSchema):
        """
        Executa a operação de salvamento.

        Args:
            t_pessoa_cartao_schema (TPessoaCartaoSchema):
                O esquema com os dados a serem persistidos.

        Returns:
            O resultado da operação de salvamento.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        t_pessoa_cartao_save_repository = TPessoaCartaoSaveRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = t_pessoa_cartao_save_repository.execute(t_pessoa_cartao_save_schema)

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return response
