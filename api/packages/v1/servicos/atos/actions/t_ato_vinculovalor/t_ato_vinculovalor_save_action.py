from abstracts.action import BaseAction
from packages.v1.servicos.atos.repositories.t_ato_vinculovalor.t_ato_vinculovalor_save_repository import (
    TAtoVinculoValorSaveRepository,
)
from packages.v1.servicos.atos.schemas.t_ato_vinculovalor_schema import (
    TAtoVinculoValorSaveSchema,
)


class TAtoVinculoValorSaveAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de salvamento de um novo registro na tabela T_ATO_VINCULOVALOR.
    """

    def execute(self, t_ato_vinculovalor_save_schema: TAtoVinculoValorSaveSchema):
        """
        Executa a operação de salvamento.

        Args:
            t_ato_vinculovalor_schema (TAtoVinculoValorSchema):
                O esquema com os dados a serem persistidos.

        Returns:
            O resultado da operação de salvamento.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        t_ato_vinculovalor_save_repository = TAtoVinculoValorSaveRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = t_ato_vinculovalor_save_repository.execute(
            t_ato_vinculovalor_save_schema
        )

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return response
