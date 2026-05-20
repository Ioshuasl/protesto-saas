from packages.v1.servicos.atos.actions.t_ato_andamento.t_ato_andamento_index_action import (
    TAtoAndamentoIndexAction,
)

from packages.v1.servicos.atos.schemas.t_ato_andamento_schema import (
    TAtoAndamentoIndexSchema,
)


class TAtoAndamentoIndexService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de registros na tabela T_ATO_ANDAMENTO.
    """

    def execute(self, data: TAtoAndamentoIndexSchema):
        """
        Executa a operação de busca de todos os registros no banco de dados.

        Args:
            t_ato_andamento_index_schema (TAtoAndamentoIndexSchema):
                Esquema que pode conter filtros ou parâmetros de busca.

        Returns:
            A lista de registros encontrados.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        t_ato_andamento_index_action = TAtoAndamentoIndexAction()

        # ----------------------------------------------------
        # Execução da ação
        # ----------------------------------------------------
        data = t_ato_andamento_index_action.execute(data)

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return data
