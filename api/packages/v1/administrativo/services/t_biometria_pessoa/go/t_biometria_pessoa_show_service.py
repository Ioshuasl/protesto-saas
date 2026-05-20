from packages.v1.administrativo.actions.t_biometria_pessoa.t_biometria_pessoa_show_action import (
    TBiometriaPessoaShowAction,
)
from packages.v1.administrativo.schemas.t_biometria_pessoa_schema import (
    TBiometriaPessoaIdSchema,
)
from fastapi import HTTPException, status


class TBiometriaPessoaShowService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela T_BIOMETRIA_PESSOA.
    """

    def execute(self, t_biometria_pessoa_id_schema: TBiometriaPessoaIdSchema):
        """
        Executa a operação de busca no banco de dados.

        Args:
            t_biometria_pessoa_id_schema (TBiometriaPessoaIdSchema):
                O esquema com o ID do registro a ser buscado.

        Returns:
            O resultado da busca.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        t_biometria_pessoa_show_action = TBiometriaPessoaShowAction()

        # ----------------------------------------------------
        # Execução da ação
        # ----------------------------------------------------
        data = t_biometria_pessoa_show_action.execute(t_biometria_pessoa_id_schema)

        # ----------------------------------------------------
        # Verificação de resultado
        # ----------------------------------------------------
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar o registro de T_BIOMETRIA_PESSOA.",
            )

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return data
