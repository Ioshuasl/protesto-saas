from packages.v1.servicos.atos.actions.t_ato_tipo.t_ato_tipo_index_action import (
    TAtoTipoIndexAction,
)


class TAtoTipoIndexService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de registros na tabela T_ATO_TIPO.
    """

    def execute(self):
        """
        Executa a operação de busca de todos os registros no banco de dados.

        Args:
            t_ato_tipo_index_schema (TAtoTipoIndexSchema):
                Esquema que pode conter filtros ou parâmetros de busca.

        Returns:
            A lista de registros encontrados.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        t_ato_tipo_index_action = TAtoTipoIndexAction()

        # ----------------------------------------------------
        # Execução da ação
        # ----------------------------------------------------
        data = t_ato_tipo_index_action.execute()

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return data
