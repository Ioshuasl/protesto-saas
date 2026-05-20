from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_biometria_pessoa.t_biometria_pessoa_save_repository import (
    TBiometriaPessoaSaveRepository,
)
from packages.v1.administrativo.schemas.t_biometria_pessoa_schema import (
    TBiometriaPessoaSaveSchema,
)


class TBiometriaPessoaSaveAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de salvamento de um novo registro na tabela T_BIOMETRIA_PESSOA.
    """

    def execute(self, t_biometria_pessoa_save_schema: TBiometriaPessoaSaveSchema):
        """
        Executa a operação de salvamento.

        Args:
            t_biometria_pessoa_schema (TBiometriaPessoaSchema):
                O esquema com os dados a serem persistidos.

        Returns:
            O resultado da operação de salvamento.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        t_biometria_pessoa_save_repository = TBiometriaPessoaSaveRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = t_biometria_pessoa_save_repository.execute(
            t_biometria_pessoa_save_schema
        )

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return response
