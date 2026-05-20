from abstracts.action import BaseAction
from packages.v1.servicos.atos.repositories.t_ato_parteimovel.t_ato_parteimovel_index_repository import (
    TAtoParteImovelIndexRepository,
)
from packages.v1.servicos.atos.schemas.t_ato_parteimovel_schema import (
    TAtoParteImovelIndexSchema,
)


class TAtoParteImovelIndexAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de todos os registros na tabela G_NATUREZA_TITULO.
    """

    def execute(self, data: TAtoParteImovelIndexSchema):
        """
        Executa a operação de listagem no banco de dados.

        Args:
            t_ato_parteimovel_index_schema (TAtoParteImovelIndexSchema):
                Esquema contendo parâmetros opcionais de filtro.

        Returns:
            A lista de registros encontrados.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        t_ato_parteimovel_index_repository = TAtoParteImovelIndexRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = t_ato_parteimovel_index_repository.execute(data)

        # ----------------------------------------------------
        # Retorno da informação
        # --------------------------------
        return response
