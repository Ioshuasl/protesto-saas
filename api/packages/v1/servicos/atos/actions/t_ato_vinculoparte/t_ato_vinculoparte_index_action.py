from abstracts.action import BaseAction
from packages.v1.servicos.atos.repositories.t_ato_vinculoparte.t_ato_vinculoparte_index_repository import (
    TAtoVinculoParteIndexRepository,
)
from packages.v1.servicos.atos.schemas.t_ato_vinculoparte_schema import (
    TAtoVinculoParteIndexSchema,
)


class TAtoVinculoParteIndexAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de todos os registros na tabela G_NATUREZA_TITULO.
    """

    def execute(self, data: TAtoVinculoParteIndexSchema):
        """
        Executa a operação de listagem no banco de dados.

        Args:
            t_ato_vinculoparte_index_schema (TAtoVinculoParteIndexSchema):
                Esquema contendo parâmetros opcionais de filtro.

        Returns:
            A lista de registros encontrados.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        t_ato_vinculoparte_index_repository = TAtoVinculoParteIndexRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = t_ato_vinculoparte_index_repository.execute(data)

        # ----------------------------------------------------
        # Retorno da informação
        # --------------------------------
        return response
