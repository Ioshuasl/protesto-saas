from packages.v1.administrativo.actions.t_pessoa.t_pessoa_show_action import TPessoaShowAction
from packages.v1.administrativo.schemas.t_pessoa_schema import TPessoaIdSchema
from packages.v1.servicos.balcao.actions.t_servico_pedido.t_servico_pedido_show_action import (
    TServicoPedidoShowAction,
)
from packages.v1.servicos.balcao.schemas.t_servico_pedido_schema import (
    TServicoPedidoIdSchema,
)
from fastapi import HTTPException, status


class TServicoPedidoShowService:

    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela T_SERVICO_PEDIDO.
    """

    def execute(self, t_servico_pedido_id_schema: TServicoPedidoIdSchema):

        """
        Executa a operação de busca no banco de dados.

        Args:
            t_servico_pedido_id_schema (TServicoPedidoIdSchema):
                O esquema com o ID do registro a ser buscado.

        Returns:
            O resultado da busca.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        t_servico_pedido_show_action = TServicoPedidoShowAction()

        # ----------------------------------------------------
        # Execução da ação
        # ----------------------------------------------------
        data = t_servico_pedido_show_action.execute(t_servico_pedido_id_schema)

        # ----------------------------------------------------
        # Verificação de resultado
        # ----------------------------------------------------
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar o registro de T_SERVICO_PEDIDO.",
            )

        # Busca os dados da pessoa vinculado a nota fiscal
        if data.pessoa_id_nfse:

            data.pessoa_nfse = TPessoaShowAction().execute(
                TPessoaIdSchema(
                    pessoa_id=data.pessoa_id_nfse
                )
            )

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return data
