from packages.v1.administrativo.actions.t_biometria_pessoa.t_biometria_pessoa_index_action import (
    TBiometriaPessoaIndexAction,
)
from fastapi import HTTPException, status

from packages.v1.administrativo.schemas.t_biometria_pessoa_schema import (
    TBiometriaPessoaIndexSchema,
)


class TBiometriaPessoaIndexService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de registros na tabela T_BIOMETRIA_PESSOA.
    """

    def execute(self, biometria_pessoa_index_schema: TBiometriaPessoaIndexSchema):
        """
        Executa a operação de busca de todos os registros no banco de dados.

        Args:
            t_biometria_pessoa_index_schema (TBiometriaPessoaIndexSchema):
                Esquema que pode conter filtros ou parâmetros de busca.

        Returns:
            A lista de registros encontrados.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        t_biometria_pessoa_index_action = TBiometriaPessoaIndexAction()

        # ----------------------------------------------------
        # Execução da ação
        # ----------------------------------------------------
        data = t_biometria_pessoa_index_action.execute(biometria_pessoa_index_schema)

        # ----------------------------------------------------
        # Verificação de retorno
        # ----------------------------------------------------
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar registros de T_BIOMETRIA_PESSOA.",
            )

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return data
