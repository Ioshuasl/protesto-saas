from abstracts.action import BaseAction
from packages.v1.servicos.balcao.repositories.t_pessoa_cartao.t_pessoa_cartao_delete_repository import (
    TPessoaCartaoDeleteRepository,
)
from packages.v1.servicos.balcao.schemas.t_pessoa_cartao_schema import (
    TPessoaCartaoIdSchema,
)


class TPessoaCartaoDeleteAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de exclusão de um registro na tabela T_PESSOA_CARTAO.
    """

    def execute(self, t_pessoa_cartao_id_schema: TPessoaCartaoIdSchema):
        """
        Executa a operação de exclusão no banco de dados.

        Args:
            t_pessoa_cartao_id_schema (TPessoaCartaoIdSchema):
                O esquema contendo o ID do registro a ser excluído.

        Returns:
            O resultado da operação de exclusão.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        t_pessoa_cartao_delete_repository = TPessoaCartaoDeleteRepository()

        # ----------------------------------------------------
        # Execução da exclusão
        # ----------------------------------------------------
        response = t_pessoa_cartao_delete_repository.execute(t_pessoa_cartao_id_schema)

        return response
