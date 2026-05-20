from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_pessoa.t_pessoa_save_repository import (
    TPessoaSaveRepository,
)
from packages.v1.administrativo.schemas.t_pessoa_schema import TPessoaSaveSchema


class TPessoaSaveAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de salvar um novo registro na tabela g_tb_regimebens.
    """

    def execute(self, t_pessoa_save_schema: TPessoaSaveSchema):
        """
        Executa a operação de salvamento.

        Args:
            regimebens_schema (GTbRegimebensSaveSchema): O esquema com os dados a serem salvos.

        Returns:
            O resultado da operação de salvamento.
        """
        # Instânciamento do repositório
        t_pessoa_save_repository = TPessoaSaveRepository()

        # Execução do repositório
        response = t_pessoa_save_repository.execute(t_pessoa_save_schema)

        # Retorno da informação
        return response
