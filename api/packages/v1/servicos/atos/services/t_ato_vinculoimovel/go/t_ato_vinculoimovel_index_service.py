from packages.v1.servicos.atos.actions.t_ato_vinculoimovel.t_ato_vinculoimovel_index_action import (
    TAtoVinculoImovelIndexAction,
)

from packages.v1.servicos.atos.schemas.t_ato_vinculoimovel_schema import (
    TAtoVinculoImovelIndexSchema,
)


class TAtoVinculoImovelIndexService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de registros na tabela T_ATO_VINCULOIMOVEL.
    """

    def execute(self, data: TAtoVinculoImovelIndexSchema):
        """
        Executa a operação de busca de todos os registros no banco de dados.

        Args:
            t_ato_vinculoimovel_index_schema (TAtoVinculoImovelIndexSchema):
                Esquema que pode conter filtros ou parâmetros de busca.

        Returns:
            A lista de registros encontrados.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        t_ato_vinculoimovel_index_action = TAtoVinculoImovelIndexAction()

        # ----------------------------------------------------
        # Execução da ação
        # ----------------------------------------------------
        data = t_ato_vinculoimovel_index_action.execute(data)

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return data
