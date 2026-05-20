from fastapi import HTTPException, status

from packages.v1.administrativo.actions.t_pessoa.t_pessoa_show_action import (
    TPessoaShowAction,
)
from packages.v1.administrativo.actions.t_servico_tipo.t_servico_tipo_show_action import (
    ShowAction,
)
from packages.v1.administrativo.schemas.g_calculo_schema import GCalculoServico
from packages.v1.administrativo.schemas.t_pessoa_schema import TPessoaIdSchema
from packages.v1.administrativo.schemas.t_servico_tipo_schema import (
    TServicoTipoIdSchema,
)
from packages.v1.administrativo.services.g_calculo.go.g_calculo_servico_service import (
    GCalculoServicoService,
)
from packages.v1.servicos.balcao.actions.t_servico_itempedido.t_servico_itempedido_show_action import (
    TServicoItemPedidoShowAction,
)
from packages.v1.servicos.balcao.actions.t_servico_itempedido.t_servico_itempedido_update_action import (
    TServicoItemPedidoUpdateAction,
)
from packages.v1.servicos.balcao.schemas.t_servico_itempedido_schema import (
    TServicoItemPedidoIdSchema,
    TServicoItemPedidoQuantidadeSchema,
    TServicoItemPedidoUpdateSchema,
)
from packages.v1.servicos.balcao.schemas.t_servico_pedido_schema import (
    TServicoPedidoUpdateValorTotal,
)
from packages.v1.servicos.balcao.services.t_servico_pedido.go.t_servico_pedido_update_valor_total_service import (
    TServicoPedidoUpdateValorTotalService,
)


class TServicoItemPedidoQuantidadeAtualizarService:

    def execute(self, data: TServicoItemPedidoQuantidadeSchema):

        # Busca item
        item = TServicoItemPedidoShowAction().execute(
            TServicoItemPedidoIdSchema(servico_itempedido_id=data.servico_itempedido_id)
        )

        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item do pedido não localizado.",
            )
        # Cálculo correto do item
        calculo = GCalculoServicoService().execute(
            GCalculoServico(
                emolumento_id=item.emolumento_id,
                quantidade=data.qtd,
                sistema_id=2,
                valor_documento=1,
            )
        )
        # O cálculo retorna valores TOTAIS.
        # O banco deve armazenar valores UNITÁRIOS.
        item.valor = calculo.valor_total / data.qtd
        item.taxa_judiciaria = calculo.valor_taxa_judiciaria / data.qtd
        item.valor_iss = calculo.valor_iss / data.qtd
        item.emolumento = calculo.valor_emolumento / data.qtd
        item.fundesp = calculo.valor_fundos / data.qtd
        item.qtd = data.qtd
        # Persistência segura do item
        item_update = TServicoItemPedidoUpdateSchema(
            servico_itempedido_id=item.servico_itempedido_id,
            valor=item.valor,
            taxa_judiciaria=item.taxa_judiciaria,
            valor_iss=item.valor_iss,
            emolumento=item.emolumento,
            fundesp=item.fundesp,
            qtd=item.qtd,
        )

        # Resposta da atualização
        update_response = TServicoItemPedidoUpdateAction().execute(item_update)

        # Verifica se existe resposta
        if not update_response:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Falha ao atualizar item.",
            )
        # Recalcula o total do pedido
        TServicoPedidoUpdateValorTotalService().execute(
            TServicoPedidoUpdateValorTotal(servico_pedido_id=item.servico_pedido_id)
        )
        # Subview (mantida)
        if getattr(item, "pessoa_id", None):

            pessoa = TPessoaShowAction().execute(
                TPessoaIdSchema(pessoa_id=item.pessoa_id)
            )

            servico_tipo = ShowAction().execute(
                TServicoTipoIdSchema(servico_tipo_id=item.servico_tipo_id)
            )

            pessoa.servico_tipo = servico_tipo
            item.subview = pessoa

        # Remoção de texto desnecessário
        item.etiqueta_texto = ""
        item.certidao_texto = ""

        return item
