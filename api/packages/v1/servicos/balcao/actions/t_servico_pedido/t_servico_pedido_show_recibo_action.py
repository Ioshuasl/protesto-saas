from abstracts.action import BaseAction
from packages.v1.parametros.schemas.g_config_schema import GConfigShowByBreadcumbSchema
from packages.v1.parametros.services.g_config.g_config_show_by_breadcumb_service import (
    GConfigShowByBreadcumbService,
)


class TServicoPedidoShowReciboAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a exibição
    de um registro na tabela G_NATUREZA_TITULO.
    """

    def execute(self):

        g_config_service = GConfigShowByBreadcumbService()

        response = g_config_service.execute(
            GConfigShowByBreadcumbSchema(
                grupo_descricao="SAAS",
                nome="RECIBO_MODELO_1",
                secao="PEDIDO",
                sistema_id=2,
            )
        )

        return response
