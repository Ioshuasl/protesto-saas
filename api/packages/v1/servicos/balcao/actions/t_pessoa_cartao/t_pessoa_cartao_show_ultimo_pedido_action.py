from abstracts.action import BaseAction
from packages.v1.servicos.balcao.repositories.t_pessoa_cartao.t_pessoa_cartao_show_ultimo_pedido_repository import (
    TPessoaCartaoShowUltimoPedidoRepository,
)
from packages.v1.servicos.balcao.schemas.t_pessoa_cartao_schema import (
    TPessoaCartaoIndexchema,
)


class TPessoaCartaoShoUltimoPedidoAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a exibição
    de um registro na tabela G_NATUREZA_TITULO.
    """

    def execute(self, data: TPessoaCartaoIndexchema):
        """
        Executa a operação de exibição.

        Args:
            t_pessoa_cartao_id_schema (TPessoaCartaoIdSchema):
                O esquema com o ID do registro a ser exibido.

        Returns:
            O resultado da operação de exibição.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        show_repository = TPessoaCartaoShowUltimoPedidoRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = show_repository.execute(data)

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return response
