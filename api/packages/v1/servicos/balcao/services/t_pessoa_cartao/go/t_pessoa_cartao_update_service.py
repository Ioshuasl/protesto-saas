from packages.v1.servicos.balcao.actions.t_pessoa_cartao.t_pessoa_cartao_update_action import (
    TPessoaCartaoUpdateAction,
)
from packages.v1.servicos.balcao.schemas.t_pessoa_cartao_schema import (
    TPessoaCartaoUpdateSchema,
)


class TPessoaCartaoUpdateService:
    """
    Serviço responsável pela operação de atualização de um registro
    na tabela T_PESSOA_CARTAO.
    """

    def execute(self, t_pessoa_cartao_update_schema: TPessoaCartaoUpdateSchema):
        """
        Executa a operação de atualização no banco de dados.

        Args:
            t_pessoa_cartao_update_schema (TPessoaCartaoUpdateSchema):
                O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        t_pessoa_cartao_update_action = TPessoaCartaoUpdateAction()

        # ----------------------------------------------------
        # Execução da ação e retorno do resultado
        # ----------------------------------------------------
        return t_pessoa_cartao_update_action.execute(t_pessoa_cartao_update_schema)
