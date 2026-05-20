from abstracts.action import BaseAction
from packages.v1.servicos.atos.repositories.t_ato_vinculoparte.t_ato_vinculoparte_save_repository import (
    TAtoVinculoParteSaveRepository,
)
from packages.v1.servicos.atos.schemas.t_ato_vinculoparte_schema import (
    TAtoVinculoParteSaveSchema,
)


class TAtoVinculoParteSaveAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de salvamento de um novo registro na tabela T_ATO_VINCULOPARTE.
    """

    def execute(self, t_ato_vinculoparte_save_schema: TAtoVinculoParteSaveSchema):
        """
        Executa a operação de salvamento.

        Args:
            t_ato_vinculoparte_schema (TAtoVinculoParteSchema):
                O esquema com os dados a serem persistidos.

        Returns:
            O resultado da operação de salvamento.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        t_ato_vinculoparte_save_repository = TAtoVinculoParteSaveRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = t_ato_vinculoparte_save_repository.execute(
            t_ato_vinculoparte_save_schema
        )

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return response
