from packages.v1.administrativo.actions.t_biometria_pessoa.t_biometria_pessoa_update_action import (
    TBiometriaPessoaUpdateAction,
)
from packages.v1.administrativo.schemas.t_biometria_pessoa_schema import (
    TBiometriaPessoaUpdateSchema,
)


class TBiometriaPessoaUpdateService:
    """
    Serviço responsável pela operação de atualização de um registro
    na tabela T_BIOMETRIA_PESSOA.
    """

    def execute(self, t_biometria_pessoa_update_schema: TBiometriaPessoaUpdateSchema):
        """
        Executa a operação de atualização no banco de dados.

        Args:
            t_biometria_pessoa_update_schema (TBiometriaPessoaUpdateSchema):
                O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        t_biometria_pessoa_update_action = TBiometriaPessoaUpdateAction()

        # ----------------------------------------------------
        # Execução da ação e retorno do resultado
        # ----------------------------------------------------
        return t_biometria_pessoa_update_action.execute(
            t_biometria_pessoa_update_schema
        )
