from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_biometria_pessoa.t_biometria_pessoa_update_repository import (
    TBiometriaPessoaUpdateRepository,
)
from packages.v1.administrativo.schemas.t_biometria_pessoa_schema import (
    TBiometriaPessoaUpdateSchema,
)


class TBiometriaPessoaUpdateAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a atualização
    de um registro na tabela G_NATUREZA_TITULO.
    """

    def execute(self, t_biometria_pessoa_update_schema: TBiometriaPessoaUpdateSchema):
        """
        Executa a operação de atualização.

        Args:
            t_biometria_pessoa_update_schema (TBiometriaPessoaUpdateSchema):
                O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório de atualização
        # ----------------------------------------------------
        t_biometria_pessoa_update_repository = TBiometriaPessoaUpdateRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = t_biometria_pessoa_update_repository.execute(
            t_biometria_pessoa_update_schema
        )

        # ----------------------------------------------------
        # Retorno do resultado
        # ----------------------------------------------------
        return response
