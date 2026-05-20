from packages.v1.servicos.balcao.actions.t_pessoa_cartao.t_pessoa_cartao_show_ultimo_pedido_action import (
    TPessoaCartaoShowAction,
)
from packages.v1.servicos.balcao.schemas.t_pessoa_cartao_schema import (
    TPessoaCartaoIdSchema,
)
from fastapi import HTTPException, status


class TPessoaCartaoShowService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela T_PESSOA_CARTAO.
    """

    def execute(self, t_pessoa_cartao_id_schema: TPessoaCartaoIdSchema):
        """
        Executa a operação de busca no banco de dados.

        Args:
            t_pessoa_cartao_id_schema (TPessoaCartaoIdSchema):
                O esquema com o ID do registro a ser buscado.

        Returns:
            O resultado da busca.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        t_pessoa_cartao_show_action = TPessoaCartaoShowAction()

        # ----------------------------------------------------
        # Execução da ação
        # ----------------------------------------------------
        data = t_pessoa_cartao_show_action.execute(t_pessoa_cartao_id_schema)

        # ----------------------------------------------------
        # Verificação de resultado
        # ----------------------------------------------------
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar o registro de T_PESSOA_CARTAO.",
            )

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return data
