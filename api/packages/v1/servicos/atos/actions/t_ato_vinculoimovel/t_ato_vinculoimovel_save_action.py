from abstracts.action import BaseAction
from packages.v1.servicos.atos.repositories.t_ato_vinculoimovel.t_ato_vinculoimovel_save_repository import (
    TAtoVinculoImovelSaveRepository,
)
from packages.v1.servicos.atos.schemas.t_ato_vinculoimovel_schema import (
    TAtoVinculoImovelSaveSchema,
)


class TAtoVinculoImovelSaveAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de salvamento de um novo registro na tabela T_ATO_VINCULOIMOVEL.
    """

    def execute(self, t_ato_vinculoimovel_save_schema: TAtoVinculoImovelSaveSchema):
        """
        Executa a operação de salvamento.

        Args:
            t_ato_vinculoimovel_schema (TAtoVinculoImovelSchema):
                O esquema com os dados a serem persistidos.

        Returns:
            O resultado da operação de salvamento.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        t_ato_vinculoimovel_save_repository = TAtoVinculoImovelSaveRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = t_ato_vinculoimovel_save_repository.execute(
            t_ato_vinculoimovel_save_schema
        )

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return response
