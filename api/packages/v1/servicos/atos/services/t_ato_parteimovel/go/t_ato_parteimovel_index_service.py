from packages.v1.servicos.atos.actions.t_ato_parteimovel.t_ato_parteimovel_index_action import (
    TAtoParteImovelIndexAction,
)

from packages.v1.servicos.atos.schemas.t_ato_parteimovel_schema import (
    TAtoParteImovelIndexSchema,
)


class TAtoParteImovelIndexService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de registros na tabela T_ATO_PARTEIMOVEL.
    """

    def execute(self, data: TAtoParteImovelIndexSchema):
        """
        Executa a operação de busca de todos os registros no banco de dados.

        Args:
            t_ato_parteimovel_index_schema (TAtoParteImovelIndexSchema):
                Esquema que pode conter filtros ou parâmetros de busca.

        Returns:
            A lista de registros encontrados.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        t_ato_parteimovel_index_action = TAtoParteImovelIndexAction()

        # ----------------------------------------------------
        # Execução da ação
        # ----------------------------------------------------
        data = t_ato_parteimovel_index_action.execute(data)

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return data
