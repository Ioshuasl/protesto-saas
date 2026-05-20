from abstracts.action import BaseAction
from packages.v1.servicos.atos.repositories.t_ato_vinculovalor.t_ato_vinculovalor_delete_repository import (
    TAtoVinculoValorDeleteRepository,
)
from packages.v1.servicos.atos.schemas.t_ato_vinculovalor_schema import (
    TAtoVinculoValorIdSchema,
)


class TAtoVinculoValorDeleteAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de exclusão de um registro na tabela T_ATO_VINCULOVALOR.
    """

    def execute(self, t_ato_vinculovalor_id_schema: TAtoVinculoValorIdSchema):
        """
        Executa a operação de exclusão no banco de dados.

        Args:
            t_ato_vinculovalor_id_schema (TAtoVinculoValorIdSchema):
                O esquema contendo o ID do registro a ser excluído.

        Returns:
            O resultado da operação de exclusão.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        t_ato_vinculovalor_delete_repository = TAtoVinculoValorDeleteRepository()

        # ----------------------------------------------------
        # Execução da exclusão
        # ----------------------------------------------------
        response = t_ato_vinculovalor_delete_repository.execute(
            t_ato_vinculovalor_id_schema
        )

        return response
