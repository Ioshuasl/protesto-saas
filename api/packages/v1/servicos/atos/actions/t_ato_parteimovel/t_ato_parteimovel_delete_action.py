from abstracts.action import BaseAction
from packages.v1.servicos.atos.repositories.t_ato_parteimovel.t_ato_parteimovel_delete_repository import (
    TAtoParteImovelDeleteRepository,
)
from packages.v1.servicos.atos.schemas.t_ato_parteimovel_schema import (
    TAtoParteImovelIdSchema,
)


class TAtoParteImovelDeleteAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de exclusão de um registro na tabela T_ATO_PARTEIMOVEL.
    """

    def execute(self, t_ato_parteimovel_id_schema: TAtoParteImovelIdSchema):
        """
        Executa a operação de exclusão no banco de dados.

        Args:
            t_ato_parteimovel_id_schema (TAtoParteImovelIdSchema):
                O esquema contendo o ID do registro a ser excluído.

        Returns:
            O resultado da operação de exclusão.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        t_ato_parteimovel_delete_repository = TAtoParteImovelDeleteRepository()

        # ----------------------------------------------------
        # Execução da exclusão
        # ----------------------------------------------------
        response = t_ato_parteimovel_delete_repository.execute(
            t_ato_parteimovel_id_schema
        )

        return response
