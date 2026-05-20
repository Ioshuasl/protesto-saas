from abstracts.action import BaseAction
from packages.v1.servicos.atos.repositories.t_ato_vinculoparte.t_ato_vinculoparte_delete_repository import (
    TAtoVinculoParteDeleteRepository,
)
from packages.v1.servicos.atos.schemas.t_ato_vinculoparte_schema import (
    TAtoVinculoParteIdSchema,
)


class TAtoVinculoParteDeleteAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de exclusão de um registro na tabela T_ATO_VINCULOPARTE.
    """

    def execute(self, t_ato_vinculoparte_id_schema: TAtoVinculoParteIdSchema):
        """
        Executa a operação de exclusão no banco de dados.

        Args:
            t_ato_vinculoparte_id_schema (TAtoVinculoParteIdSchema):
                O esquema contendo o ID do registro a ser excluído.

        Returns:
            O resultado da operação de exclusão.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        t_ato_vinculoparte_delete_repository = TAtoVinculoParteDeleteRepository()

        # ----------------------------------------------------
        # Execução da exclusão
        # ----------------------------------------------------
        response = t_ato_vinculoparte_delete_repository.execute(
            t_ato_vinculoparte_id_schema
        )

        return response
