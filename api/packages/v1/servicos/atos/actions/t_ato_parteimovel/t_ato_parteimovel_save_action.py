from abstracts.action import BaseAction
from packages.v1.servicos.atos.repositories.t_ato_parteimovel.t_ato_parteimovel_save_repository import (
    TAtoParteImovelSaveRepository,
)
from packages.v1.servicos.atos.schemas.t_ato_parteimovel_schema import (
    TAtoParteImovelSaveSchema,
)


class TAtoParteImovelSaveAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de salvamento de um novo registro na tabela T_ATO_PARTEIMOVEL.
    """

    def execute(self, t_ato_parteimovel_save_schema: TAtoParteImovelSaveSchema):
        """
        Executa a operação de salvamento.

        Args:
            t_ato_parteimovel_schema (TAtoParteImovelSchema):
                O esquema com os dados a serem persistidos.

        Returns:
            O resultado da operação de salvamento.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        t_ato_parteimovel_save_repository = TAtoParteImovelSaveRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = t_ato_parteimovel_save_repository.execute(
            t_ato_parteimovel_save_schema
        )

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return response
