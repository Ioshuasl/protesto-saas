from types import SimpleNamespace
from pathlib import Path

from packages.v1.docx.actions.docx_table_loop_action import DOCXTableLoopAction
from packages.v1.docx.schemas.docx_table_loop_schema import DOCXTableLoopSchema
from packages.v1.parametros.schemas.g_config_schema import GConfigShowByBreadcumbSchema
from packages.v1.parametros.services.g_config.g_config_show_by_breadcumb_service import GConfigShowByBreadcumbService
from packages.v1.resolver.schemas.resolver_schema import ResolverSchema
from packages.v1.resolver.services.resolver_main_service import ResolverMainService
from packages.v1.servicos.balcao.schemas.t_servico_itempedido_schema import (
    TServicoItemIndexSchema,
)
from packages.v1.servicos.balcao.schemas.t_servico_pedido_schema import (
    TServicoPedidoIdSchema,
)
from packages.v1.servicos.balcao.services.t_servico_itempedido.go.t_servico_itempedido_index_service import (
    TServicoItemPedidoIndexService,
)
from fastapi import HTTPException, status


class TServicoPedidoShowReciboService:

    def execute(self, data: TServicoPedidoIdSchema):

        # Obtem a configuração do recibo
        response = GConfigShowByBreadcumbService().execute(
            GConfigShowByBreadcumbSchema(
                grupo_descricao="SAAS",
                nome="RECIBO_MODELO_1",
                secao="PEDIDO",
                sistema_id=2,
            )
        )

        if not response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar a configuração do recibo.",
            )

        # Executa
        resolver_main_service_response = ResolverMainService().execute(
            ResolverSchema(
                id=data.servico_pedido_id,
                campo_id_valor=data.servico_pedido_id,
                sitema_id=2,
                texto=response.texto,
            )
        )

        itens_servico_ids = self._resolve_item_ids(data)

        recibo_path = Path("./storage/temp") / str(resolver_main_service_response)
        DOCXTableLoopAction.execute(
            DOCXTableLoopSchema(
                input_docx=str(recibo_path),
                output_docx=str(recibo_path),
                save_to_disk=True,
                collections={"itens_servico": itens_servico_ids},
                clear_when_empty=True,
            )
        )

        response = SimpleNamespace()

        response.recibo_texto = resolver_main_service_response

        return response

    def _resolve_item_ids(self, data: TServicoPedidoIdSchema) -> list:
        incoming_ids = getattr(data, "servico_itempedido_ids", None)
        if incoming_ids is None:
            incoming_ids = getattr(data, "itens_servico_ids", None)
        if incoming_ids is None:
            incoming_ids = getattr(data, "itens_servico", None)

        if isinstance(incoming_ids, list):
            return [item_id for item_id in incoming_ids if item_id is not None]

        itens_servico = TServicoItemPedidoIndexService().execute(
            TServicoItemIndexSchema(servico_pedido_id=data.servico_pedido_id)
        )
        return [
            getattr(item, "servico_itempedido_id", None)
            for item in itens_servico or []
            if getattr(item, "servico_itempedido_id", None) is not None
        ]
