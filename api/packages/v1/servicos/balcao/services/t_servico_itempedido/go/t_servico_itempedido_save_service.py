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
from packages.v1.servicos.atos.actions.t_ato.t_ato_show_action import TAtoShowAction
from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoIdSchema
from packages.v1.administrativo.services.g_calculo.go.g_calculo_servico_service import (
    GCalculoServicoService,
)
from packages.v1.servicos.balcao.actions.t_servico_itempedido.t_servico_itempedido_save_action import (
    TServicoItemPedidoSaveAction,
)
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.servicos.balcao.schemas.t_servico_itempedido_schema import (
    TServicoItemPedidoSaveSchema,
)
from packages.v1.sequencia.services.g_sequencia.generate_service import (
    GenerateService,
)
from packages.v1.servicos.balcao.schemas.t_servico_pedido_schema import (
    TServicoPedidoUpdateValorTotal,
)
from packages.v1.servicos.balcao.services.t_servico_pedido.go.t_servico_pedido_update_valor_total_service import (
    TServicoPedidoUpdateValorTotalService,
)


class TServicoItemPedidoSaveService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de criação de registros na tabela T_SERVICO_ITEMPEDIDO.
    """

    def execute(self, data: TServicoItemPedidoSaveSchema):

        # Valor para base calculo
        valor_calculo = 0

        # Verifica o tipo de valor a ser considerado
        if data.valor_base_calculo:

            valor_calculo = data.valor_base_calculo

        # Verifica o tipo de valor a ser considerado
        if data.valor_avaliacao:

            valor_calculo = data.valor_avaliacao

        # Verifica o tipo de valor a ser considerado
        if data.valor_documento:

            valor_calculo = data.valor_documento
        is_abono = data.tipo_item == "B"
        calculo_servico_response = GCalculoServicoService().execute(
            GCalculoServico(
                emolumento_id=data.emolumento_id,
                quantidade=1.0,
                sistema_id=2,
                valor_documento=valor_calculo,
            )
        )

        # Verifica se é do tipo B de Abono, se for recalculo os valores iniciais de acordom a referencia
        if is_abono:
            calculo_servico_response = GCalculoServicoService().execute(
                GCalculoServico(
                    emolumento_id=data.emolumento_id,
                    quantidade=1.0,
                    sistema_id=2,
                    valor_documento=valor_calculo,
                    codigo_tabela=calculo_servico_response.codigo_tabela,
                )
            )

        # Atualiza os valores do Item
        data.emolumento_id = calculo_servico_response.emolumento_id
        data.emolumento_item_id = calculo_servico_response.emolumento_item_id
        data.emolumento = 0 if is_abono else calculo_servico_response.valor_emolumento
        data.taxa_judiciaria = (
            0 if is_abono else calculo_servico_response.valor_taxa_judiciaria
        )
        data.valor_iss = 0 if is_abono else calculo_servico_response.valor_iss
        data.valor = 0 if is_abono else calculo_servico_response.valor_total

        # Fundesp permanece em ambos os casos
        data.fundesp = calculo_servico_response.valor_fundos
        # Geração automática de ID (sequência)
        if not data.servico_itempedido_id:

            # Cria o schema de sequência
            sequencia = GenerateService().execute(GSequenciaSchema(tabela="T_SERVICO_ITEMPEDIDO"))

            # Atualiza o ID no schema
            data.servico_itempedido_id = sequencia.sequencia
        t_servico_itempedido_save_action = TServicoItemPedidoSaveAction()
        response = t_servico_itempedido_save_action.execute(data)

        if response:

            # Classe para atualiza o valor total do pedido
            servico_pedido_update_valor_total = TServicoPedidoUpdateValorTotalService()

            # Atualiza os novos valores
            servico_pedido_update_valor_total.execute(
                TServicoPedidoUpdateValorTotal(
                    servico_pedido_id=data.servico_pedido_id,
                    valor_pedido=data.valor,
                    valor_pago=data.valor,
                    operacao=1,
                )
            )
            if getattr(response, "pessoa_id", None):
                pessoa_show_action = TPessoaShowAction()
                response.subview = pessoa_show_action.execute(
                    TPessoaIdSchema(pessoa_id=response.pessoa_id)
                )

                if response.subview and getattr(response, "servico_tipo_id", None):
                    servico_tipo_show = ShowAction()
                    response.subview.servico_tipo = servico_tipo_show.execute(
                        TServicoTipoIdSchema(servico_tipo_id=response.servico_tipo_id)
                    )
                    if response.subview.servico_tipo:
                        response.subview.servico_tipo.tipo_item = response.tipo_item

            if getattr(response, "certidao_ato_id", None):
                ato_show_action = TAtoShowAction()
                response.subview = ato_show_action.execute(
                    TAtoIdSchema(ato_id=response.certidao_ato_id)
                )

                if response.subview and getattr(response, "servico_tipo_id", None):
                    servico_tipo_show = ShowAction()
                    response.subview.servico_tipo = servico_tipo_show.execute(
                        TServicoTipoIdSchema(servico_tipo_id=response.servico_tipo_id)
                    )
                    if response.subview.servico_tipo:
                        response.subview.servico_tipo.tipo_item = response.tipo_item

                if response.subview and hasattr(response.subview, "texto"):
                    response.subview.texto = None

            # Remove os textos da resposta
            response.certidao_texto = ""
            response.etiqueta_texto = ""

        return response
