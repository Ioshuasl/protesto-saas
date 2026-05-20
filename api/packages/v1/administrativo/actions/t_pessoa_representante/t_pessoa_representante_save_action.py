from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_pessoa_representante.t_pessoa_representante_save_repository import (
    TPessoaRepresentanteSaveRepository,
)
from packages.v1.administrativo.schemas.t_pessoa_representante_schema import (
    TPessoaRepresentanteSaveSchema,
)


class TPessoaRepresentanteSaveAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de salvar um novo registro na tabela g_tb_regimebens.
    """

    def execute(
        self, t_pessoa_representante_save_schema: TPessoaRepresentanteSaveSchema
    ):
        """
        Executa a operação de salvamento.

        Args:
            regimebens_schema (GTbRegimebensSaveSchema): O esquema com os dados a serem salvos.

        Returns:
            O resultado da operação de salvamento.
        """
        # Instânciamento do repositório
        t_pessoa_representante_save_repository = TPessoaRepresentanteSaveRepository()

        # Execução do repositório
        response = t_pessoa_representante_save_repository.execute(
            t_pessoa_representante_save_schema
        )

        # Retorno da informação
        return response
