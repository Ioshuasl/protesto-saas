from packages.v1.administrativo.schemas.c_caixa_item_schema import CaixaItemSchema
from packages.v1.administrativo.services.c_caixa_item.go.c_caixa_item_save_service import (
    SaveService,
)
from packages.v1.servicos.balcao.actions.t_servico_pedido.t_servico_pedido_save_situacao_action import (
    TServicoPedidoSaveSituacaoAction,
)
from packages.v1.servicos.balcao.schemas.t_servico_pedido_schema import (
    TServicoPedidoSaveSituacaoSchema,
    TServicoPedidoSituacaoSchema,
)


class TServicoPedidoAtivarService:

    def execute(self, data: TServicoPedidoSituacaoSchema):

        # Instancia corretamente a Action (classe)
        save_situacao_action = TServicoPedidoSaveSituacaoAction()

        # Executa o fluxo da action com o schema recebido
        response = save_situacao_action.execute(
            data=TServicoPedidoSaveSituacaoSchema(
                servico_pedido_id=data.servico_pedido_id, situacao="F"
            )
        )

        if response:

            # Controle de pedidos
            c_caixa_item_save_service = SaveService()

            # Salva o serviço no caixa
            c_caixa_item_save_service.execute(
                CaixaItemSchema(
                    apresentante=response.apresentante,
                    usuario_servico_id=data.usuario_id,
                    chave_servico=response.servico_pedido_id,
                    descricao="Ativação do Pedido",
                    situacao=3,
                    tipo_transacao="C",
                    valor_servico=response.valor_pedido,
                    valor_pago=response.valor_pago,
                )
            )

        return response
