from packages.v1.servicos.balcao.actions.t_pessoa_cartao.t_pessoa_cartao_index_action import (
    TPessoaCartaoIndexAction,
)
from fastapi import HTTPException, status

from packages.v1.servicos.balcao.schemas.t_pessoa_cartao_schema import (
    TPessoaCartaoIndexchema,
)


class TPessoaCartaoIndexService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de registros na tabela T_PESSOA_CARTAO.
    """

    def execute(self, t_pessoa_cartao_index_schema: TPessoaCartaoIndexchema):
        """
        Executa a operação de busca de todos os registros no banco de dados.

        Args:
            t_pessoa_cartao_index_schema (TPessoaCartaoIndexSchema):
                Esquema que pode conter filtros ou parâmetros de busca.

        Returns:
            A lista de registros encontrados.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        t_pessoa_cartao_index_action = TPessoaCartaoIndexAction()

        # ----------------------------------------------------
        # Execução da ação
        # ----------------------------------------------------
        data = t_pessoa_cartao_index_action.execute(t_pessoa_cartao_index_schema)

        # ----------------------------------------------------
        # Verificação de retorno
        # ----------------------------------------------------
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar registros de T_PESSOA_CARTAO.",
            )

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return data
