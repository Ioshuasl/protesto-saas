from packages.v1.servicos.atos.actions.t_ato_vinculovalor.t_ato_vinculovalor_index_action import (
    TAtoVinculoValorIndexAction,
)

from packages.v1.servicos.atos.schemas.t_ato_vinculovalor_schema import (
    TAtoVinculoValorIndexSchema,
)


class TAtoVinculoValorIndexService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de registros na tabela T_ATO_VINCULOVALOR.
    """

    def execute(self, data: TAtoVinculoValorIndexSchema):
        """
        Executa a operação de busca de todos os registros no banco de dados.

        Args:
            t_ato_vinculovalor_index_schema (TAtoVinculoValorIndexSchema):
                Esquema que pode conter filtros ou parâmetros de busca.

        Returns:
            A lista de registros encontrados.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        t_ato_vinculovalor_index_action = TAtoVinculoValorIndexAction()

        # ----------------------------------------------------
        # Execução da ação
        # ----------------------------------------------------
        data = t_ato_vinculovalor_index_action.execute(data)

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return data
