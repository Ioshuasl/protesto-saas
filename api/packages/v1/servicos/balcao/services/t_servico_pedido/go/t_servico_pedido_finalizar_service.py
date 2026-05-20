from datetime import datetime
from decimal import Decimal
import json

from actions.data.sha_256_crypt import Sha256Crypt
from packages.v1.nfse.schemas.nfse_schema import NfseSaveSchema
from packages.v1.nfse.services.nfse_save_service import NfseSaveService
from packages.v1.servicos.atos.schemas.t_historico_schema import THistoricoSaveSchema
from packages.v1.servicos.atos.services.t_historico.go.t_historico_save_service import (
    THistoricoSaveService,
)
from packages.v1.servicos.balcao.actions.t_servico_pedido.t_servico_pedido_save_situacao_action import (
    TServicoPedidoSaveSituacaoAction,
)
from packages.v1.servicos.balcao.schemas.t_servico_itempedido_schema import (
    TServicoItemIndexSchema,
)
from packages.v1.servicos.balcao.schemas.t_servico_pedido_schema import (
    TServicoPedidoIdSchema,
    TServicoPedidoSaveSituacaoSchema,
)
from packages.v1.servicos.balcao.services.t_servico_itempedido.go.t_servico_itempedido_finalizar_todos_service import (
    TServicoItemPedidoFinalizarTodosService,
)


class TServicoPedidoFinalizarService:

    def execute(self, data: TServicoPedidoIdSchema):

        # Executa o fluxo da action com o schema recebido
        response = TServicoPedidoSaveSituacaoAction().execute(
            data=TServicoPedidoSaveSituacaoSchema(
                servico_pedido_id=data.servico_pedido_id, situacao="F"
            )
        )

        if response:

            # Gera selo e coloca como finalizado todos os itens do pedido
            TServicoItemPedidoFinalizarTodosService().execute(
                TServicoItemIndexSchema(
                    servico_pedido_id=data.servico_pedido_id, usuario_id=data.usuario_id
                )
            )

            now = datetime.now()

            # Atualiza o histórioc do caixa
            THistoricoSaveService().execute(
                THistoricoSaveSchema(
                    tabela="T_SERVICO_PEDIDO",
                    hash=Sha256Crypt.execute(f"TSP_{response.servico_pedido_id}"),
                    campo="Pedido de balcao finalizado",
                    operacao="U",
                    new_value=json.dumps(response, default=str),
                    usuario_id=data.usuario_id,
                    data=now,
                    id=response.servico_pedido_id,
                    observacao=(
                        "Pedido de balcao finalizado com itens processados "
                        "e nota fiscal solicitada"
                    ),
                    data_registro=None,
                    dados_complementares=None,
                )
            )

            # Criação da nota fiscal
            NfseSaveService().execute(
                NfseSaveSchema(
                    id_cliente=getattr(response, "pessoa_id", None),
                    data_hora=datetime.now(),
                    dataemissao=datetime.now(),
                    total_servicos=(getattr(response, "valor_pago", None)),
                    total_liquido=(getattr(response, "valor_pago", None)),
                    valor_iss=Decimal("0"),
                    discriminacao=(
                        "Servicos de Balcao do Tabelionato de Notas: "
                        f"Pedido {response.servico_pedido_id}"
                    ),
                    tomador_razao_social=(getattr(response, "apresentante", None)),
                    tomador_cnpj=getattr(response, "cpfcnpj_apresentante", None),
                )
            )

        return response
