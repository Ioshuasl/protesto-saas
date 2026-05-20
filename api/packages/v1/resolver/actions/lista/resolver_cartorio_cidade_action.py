from packages.v1.parametros.actions.g_config.g_config_show_by_breadcumb_action import (
    GConfigShowByBreadcumbAction,
)
from packages.v1.parametros.schemas.g_config_schema import GConfigShowByBreadcumbSchema


class ResolverCartorioCidadeAction:

    @staticmethod
    def execute():

        return (
            GConfigShowByBreadcumbAction()
            .execute(
                GConfigShowByBreadcumbSchema(
                    grupo_descricao="PRINCIPAL",
                    secao="CARTORIO",
                    nome="CIDADE",
                    sistema_id=2,
                )
            )
            .valor
        )
