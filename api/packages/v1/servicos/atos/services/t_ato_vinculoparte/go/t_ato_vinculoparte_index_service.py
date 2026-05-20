from packages.v1.servicos.atos.actions.t_ato_vinculoparte.t_ato_vinculoparte_index_action import (
    TAtoVinculoParteIndexAction,
)

from packages.v1.servicos.atos.schemas.t_ato_vinculoparte_schema import (
    TAtoVinculoParteIndexSchema,
)


class TAtoVinculoParteIndexService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de registros na tabela T_ATO_VINCULOPARTE.
    """

    def execute(self, data: TAtoVinculoParteIndexSchema):
        """
        Executa a operação de busca de todos os registros no banco de dados.

        Args:
            t_ato_vinculoparte_index_schema (TAtoVinculoParteIndexSchema):
                Esquema que pode conter filtros ou parâmetros de busca.

        Returns:
            A lista de registros encontrados.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        t_ato_vinculoparte_index_action = TAtoVinculoParteIndexAction()

        # ----------------------------------------------------
        # Execução da ação
        # ----------------------------------------------------
        response = t_ato_vinculoparte_index_action.execute(data)

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return response
