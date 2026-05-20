from packages.v1.administrativo.schemas.c_caixa_item_schema import CaixaItemSchema
from packages.v1.administrativo.schemas.t_servico_tipo_schema import (
    TServicoTipoIdSchema,
)
from packages.v1.administrativo.services.c_caixa_item.go.c_caixa_item_save_service import (
    SaveService,
)
from packages.v1.administrativo.services.t_servico_tipo.go.t_servico_tipo_show_service import (
    ShowService,
)
from packages.v1.servicos.balcao.actions.t_servico_itempedido.t_servico_itempedido_save_situacao_action import (
    TServicoItemPedidoSaveSituacaoAction,
)
from packages.v1.servicos.balcao.schemas.t_servico_itempedido_schema import (
    TServicoItemPedidoSaveSituacaoSchema,
    TServicoItemPedidoSituacaoSchema,
)
from packages.v1.servicos.balcao.schemas.t_servico_pedido_schema import (
    TServicoPedidoIdSchema,
)
from packages.v1.servicos.balcao.services.t_servico_pedido.go.t_servico_pedido_show_service import (
    TServicoPedidoShowService,
)


class TServicoItemPedidoCancelarService:
    """
    Serviço responsável por cancelar um item de pedido de serviço,
    alterando sua situação via Action TServicoItemPedidoSaveSituacaoAction.
    """

    def execute(self, data: TServicoItemPedidoSituacaoSchema):

        # Instancia corretamente a Action (classe)
        save_situacao_action = TServicoItemPedidoSaveSituacaoAction()

        # Executa o fluxo da action com o schema recebido
        response = save_situacao_action.execute(
            TServicoItemPedidoSaveSituacaoSchema(
                servico_itempedido_id=data.servico_itempedido_id, situacao="C"
            )
        )

        pedido_show = TServicoPedidoShowService()

        # Busca o pedido
        response_pedido_show = pedido_show.execute(
            TServicoPedidoIdSchema(servico_pedido_id=response.servico_pedido_id)
        )

        if response:

            # Busca os detalhes do serviço do item
            t_servico_tipo_show = ShowService()

            response_t_servico_tipo_show = t_servico_tipo_show.execute(
                TServicoTipoIdSchema(servico_tipo_id=response.servico_tipo_id)
            )

            # Controle de pedidos
            c_caixa_item_save_service = SaveService()

            # Salva o serviço no caixa
            c_caixa_item_save_service.execute(
                CaixaItemSchema(
                    apresentante=response_pedido_show.apresentante,
                    usuario_servico_id=data.usuario_id,
                    chave_servico=response.servico_pedido_id,
                    descricao=response_t_servico_tipo_show.descricao,
                    situacao=3,
                    tipo_transacao="D",
                    emolumento_item_id=response.emolumento_item_id,
                    emolumento=response.emolumento,
                    taxa_judiciaria=response.taxa_judiciaria,
                    iss=response.valor_iss,
                    fundesp=response.fundesp,
                    valor_servico=1,
                    valor_pago=1,
                )
            )

        return response
