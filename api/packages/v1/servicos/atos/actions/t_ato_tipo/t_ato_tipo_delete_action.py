from abstracts.action import BaseAction
from packages.v1.servicos.atos.repositories.t_ato_tipo.t_ato_tipo_delete_repository import (
    TAtoTipoDeleteRepository,
)
from packages.v1.servicos.atos.schemas.t_ato_tipo_schema import (
    TAtoTipoIdSchema,
)


class TAtoTipoDeleteAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de exclusão de um registro na tabela T_ATO_TIPO.
    """

    def execute(self, t_ato_tipo_id_schema: TAtoTipoIdSchema):
        """
        Executa a operação de exclusão no banco de dados.

        Args:
            t_ato_tipo_id_schema (TAtoTipoIdSchema):
                O esquema contendo o ID do registro a ser excluído.

        Returns:
            O resultado da operação de exclusão.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        t_ato_tipo_delete_repository = TAtoTipoDeleteRepository()

        # ----------------------------------------------------
        # Execução da exclusão
        # ----------------------------------------------------
        response = t_ato_tipo_delete_repository.execute(
            t_ato_tipo_id_schema
        )

        return response
