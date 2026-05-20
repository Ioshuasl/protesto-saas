from abstracts.action import BaseAction
from packages.v1.servicos.atos.repositories.t_ato_andamento.t_ato_andamento_save_repository import (
    TAtoAndamentoSaveRepository,
)
from packages.v1.servicos.atos.schemas.t_ato_andamento_schema import (
    TAtoAndamentoSaveSchema,
)


class TAtoAndamentoSaveAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de salvamento de um novo registro na tabela T_ATO_ANDAMENTO.
    """

    def execute(self, t_ato_andamento_save_schema: TAtoAndamentoSaveSchema):
        """
        Executa a operação de salvamento.

        Args:
            t_ato_andamento_schema (TAtoAndamentoSchema):
                O esquema com os dados a serem persistidos.

        Returns:
            O resultado da operação de salvamento.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        t_ato_andamento_save_repository = TAtoAndamentoSaveRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = t_ato_andamento_save_repository.execute(
            t_ato_andamento_save_schema
        )

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return response
