from datetime import datetime
import json
from actions.data.sha_256_crypt import Sha256Crypt
from packages.v1.administrativo.schemas.c_caixa_item_schema import CaixaItemSchema
from packages.v1.administrativo.schemas.g_selo_livro_schema import (
    GSeloLivroLivreSchema,
    GSeloLivroUpdateSchema,
)
from packages.v1.administrativo.schemas.t_servico_tipo_schema import (
    TServicoTipoIdSchema,
)
from packages.v1.administrativo.services.c_caixa_item.go.c_caixa_item_save_service import (
    SaveService,
)
from packages.v1.administrativo.services.g_selo_livro.go.g_selo_livro_livre_show_service import (
    GSeloLivroLivreShowService,
)
from packages.v1.administrativo.services.g_selo_livro.go.g_selo_livro_update_service import (
    GSeloLivroUpdateService,
)
from packages.v1.servicos.atos.actions.t_historico.t_historico_save_action import (
    THistoricoSaveAction,
)
from packages.v1.servicos.atos.schemas.t_historico_schema import THistoricoSaveSchema
from packages.v1.servicos.atos.services.t_historico.go.t_historico_save_service import (
    THistoricoSaveService,
)
from packages.v1.servicos.balcao.actions.t_servico_itempedido.t_servico_itempedido_index_action import (
    TServicoItemPedidoIndexAction,
)
from packages.v1.servicos.balcao.actions.t_servico_itempedido.t_servico_itempedido_save_situacao_action import (
    TServicoItemPedidoSaveSituacaoAction,
)
from packages.v1.servicos.balcao.actions.t_servico_pedido.t_servico_pedido_show_action import (
    TServicoPedidoShowAction,
)
from packages.v1.servicos.balcao.schemas.t_pessoa_cartao_schema import (
    TPessoaCartaoUpdateSchema,
)
from packages.v1.servicos.balcao.schemas.t_servico_itempedido_schema import (
    TServicoItemPedidoSaveSituacaoSchema,
    TServicoItemIndexSchema,
)
from packages.v1.servicos.balcao.schemas.t_servico_pedido_schema import (
    TServicoPedidoIdSchema,
)

# Importação da Action ajustada
from packages.v1.administrativo.actions.t_servico_tipo.t_servico_tipo_show_action import (
    ShowAction,
)
from packages.v1.servicos.balcao.services.t_pessoa_cartao.go.t_pessoa_cartao_finalizar_service import (
    TPessoaCartaoFinalizarService,
)


class TServicoItemPedidoFinalizarTodosService:
    """
    Serviço responsável por cancelar um item de pedido de serviço,
    alterando sua situação via Action TServicoItemPedidoSaveSituacaoAction.
    """

    def execute(self, data: TServicoItemIndexSchema):

        # Busca todos os itens
        index_action_response = TServicoItemPedidoIndexAction().execute(data)

        if index_action_response:

            for item in index_action_response:

                # Atualiza a situação do item
                response = TServicoItemPedidoSaveSituacaoAction().execute(
                    TServicoItemPedidoSaveSituacaoSchema(
                        servico_itempedido_id=item.servico_itempedido_id, situacao="F"
                    )
                )

                now = datetime.now()

                # Atualiza o histórioc do caixa
                THistoricoSaveService().execute(
                    THistoricoSaveSchema(
                        tabela="T_SERVICO_ITEMPEDIDO",
                        hash=Sha256Crypt.execute(f"TSP_{response.servico_pedido_id}"),
                        campo="Item de pedido de balcao finalizado",
                        operacao="U",
                        new_value=json.dumps(response, default=str),
                        usuario_id=data.usuario_id,
                        data=now,
                        id=response.servico_itempedido_id,
                        observacao="Item de pedido de balcao marcado como finalizado",
                        data_registro=None,
                        dados_complementares=None,
                    )
                )

                if response:

                    # Busca o pedido
                    response_pedido_show = TServicoPedidoShowAction().execute(
                        TServicoPedidoIdSchema(servico_pedido_id=response.servico_pedido_id)
                    )

                    # Busca o tipo de serviço
                    response_t_servico_tipo_show = ShowAction().execute(
                        TServicoTipoIdSchema(servico_tipo_id=item.servico_tipo_id)
                    )

                    # Salva o serviço no caixa
                    response_c_caixa_item = SaveService().execute(
                        CaixaItemSchema(
                            apresentante=response_pedido_show.apresentante,
                            usuario_servico_id=data.usuario_id,
                            chave_servico=response_pedido_show.servico_pedido_id,
                            descricao=response_t_servico_tipo_show.descricao,
                            situacao=3,
                            emolumento_item_id=item.emolumento_item_id,
                            emolumento=item.emolumento,
                            taxa_judiciaria=item.taxa_judiciaria,
                            iss=item.valor_iss,
                            fundesp=item.fundesp,
                            valor_servico=1,
                            valor_pago=1,
                        )
                    )

                    now = datetime.now()

                    # Atualiza o histórioc do caixa
                    THistoricoSaveService().execute(
                        THistoricoSaveSchema(
                            tabela="C_CAIXA_ITEM",
                            hash=Sha256Crypt.execute(f"TSP_{response.servico_pedido_id}"),
                            campo="Item de pedido lancado no caixa",
                            operacao="I",
                            new_value=json.dumps(response_c_caixa_item, default=str),
                            usuario_id=data.usuario_id,
                            data=now,
                            id=response_c_caixa_item.caixa_item_id,
                            observacao=(
                                "Lancamento de caixa gerado pela finalizacao " "do item de pedido"
                            ),
                            data_registro=None,
                            dados_complementares=None,
                        )
                    )

                    for _ in range(int(item.qtd)):

                        selo_livre_response = GSeloLivroLivreShowService().execute(
                            GSeloLivroLivreSchema(selo_grupo_id=item.selo_grupo_id)
                        )

                        descricao = (
                            f"{response_t_servico_tipo_show.descricao}"
                            f"* P{response_pedido_show.servico_pedido_id} * "
                            f"{response_pedido_show.apresentante}"
                        )

                        # Executa a service
                        response_g_selo_livro = GSeloLivroUpdateService().execute(
                            GSeloLivroUpdateSchema(
                                selo_livro_id=selo_livre_response.selo_livro_id,
                                selo_situacao_id=2,
                                descricao=descricao,
                                tabela="T_SERVICO_ITEMPEDIDO",
                                campo_id=item.servico_itempedido_id,
                                usuario_id=data.usuario_id,
                                data_informacao=datetime.now(),
                                data=datetime.now(),
                                apresentante=response_pedido_show.apresentante,
                                numero_agrupador=selo_livre_response.numero_selo,
                                valor_iss=item.valor_iss,
                                valor_emolumento=item.emolumento,
                                valor_fundesp=item.fundesp,
                                valor_taxa_judiciaria=item.taxa_judiciaria,
                                valor_total=item.emolumento + item.taxa_judiciaria + item.fundesp,
                            )
                        )

                        now = datetime.now()

                        # Atualiza o histórioc do caixa
                        THistoricoSaveService().execute(
                            THistoricoSaveSchema(
                                tabela="G_SELO_LIVRO",
                                hash=Sha256Crypt.execute(f"TSP_{response.servico_pedido_id}"),
                                campo="Selo vinculado ao item de pedido",
                                operacao="U",
                                new_value=json.dumps(response_g_selo_livro, default=str),
                                usuario_id=data.usuario_id,
                                data=now,
                                id=response_g_selo_livro.selo_livro_id,
                                observacao=(
                                    "Selo consumido e vinculado ao item de pedido "
                                    "durante a finalizacao do pedido de balcao"
                                ),
                                data_registro=None,
                                dados_complementares=None,
                            )
                        )

                    # Verifica se o item é do tipo cartao
                    if item.tipo_item == "CA":

                        # Execução
                        TPessoaCartaoFinalizarService().execute(
                            TPessoaCartaoUpdateSchema(
                                pessoa_id=item.pessoa_id,
                            )
                        )

        return response
