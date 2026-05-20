from abstracts.action import BaseAction
from packages.v1.servicos.atos.repositories.t_ato.t_ato_save_repository import (
    TAtoSaveRepository,
)
from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoSaveSchema


class TAtoSaveAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de salvamento de um novo registro na tabela T_ATO.
    """

    def execute(self, t_ato_save_schema: TAtoSaveSchema):
        """
        Executa a operação de salvamento.

        Args:
            t_ato_schema (TAtoSchema):
                O esquema com os dados a serem persistidos.

        Returns:
            O resultado da operação de salvamento.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        t_ato_save_repository = TAtoSaveRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = t_ato_save_repository.execute(t_ato_save_schema)

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return response
