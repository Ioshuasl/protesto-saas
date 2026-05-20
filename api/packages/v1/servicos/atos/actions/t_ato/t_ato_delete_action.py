from abstracts.action import BaseAction
from packages.v1.servicos.atos.repositories.t_ato.t_ato_delete_repository import (
    TAtoDeleteRepository,
)
from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoIdSchema


class TAtoDeleteAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de exclusão de um registro na tabela T_ATO.
    """

    def execute(self, t_ato_id_schema: TAtoIdSchema):
        """
        Executa a operação de exclusão no banco de dados.

        Args:
            t_ato_id_schema (TAtoIdSchema):
                O esquema contendo o ID do registro a ser excluído.

        Returns:
            O resultado da operação de exclusão.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        t_ato_delete_repository = TAtoDeleteRepository()

        # ----------------------------------------------------
        # Execução da exclusão
        # ----------------------------------------------------
        response = t_ato_delete_repository.execute(t_ato_id_schema)

        return response
