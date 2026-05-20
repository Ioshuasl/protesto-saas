from packages.v1.parametros.schemas.g_config_schema import GConfigNomeSchema
from packages.v1.parametros.services.g_config.g_config_show_by_nome_service import (
    GConfigShowByNomeService,
)


class TServicoPedidoLoadParamsService:
    """
    Serviço responsável pela operação de atualização de um registro
    na tabela T_SERVICO_PEDIDO.
    """

    def execute(self):

        response = []

        g_config_show_by_nome_service = GConfigShowByNomeService()

        response.append(
            g_config_show_by_nome_service.execute(
                GConfigNomeSchema(nome="SERVICO_ABERTURA_CARTAO", sistema_id=2)
            )
        )

        return response
