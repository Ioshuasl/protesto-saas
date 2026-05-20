from abstracts.action import BaseAction
from packages.v1.servicos.atos.repositories.t_ato_vinculoimovel.t_ato_vinculoimovel_show_repository import (
    TAtoVinculoImovelShowRepository,
)
from packages.v1.servicos.atos.schemas.t_ato_vinculoimovel_schema import (
    TAtoVinculoImovelIdSchema,
)


class TAtoVinculoImovelShowAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a exibição
    de um registro na tabela G_NATUREZA_TITULO.
    """

    def execute(self, t_ato_vinculoimovel_id_schema: TAtoVinculoImovelIdSchema):
        """
        Executa a operação de exibição.

        Args:
            t_ato_vinculoimovel_id_schema (TAtoVinculoImovelIdSchema):
                O esquema com o ID do registro a ser exibido.

        Returns:
            O resultado da operação de exibição.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        t_ato_vinculoimovel_show_repository = TAtoVinculoImovelShowRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = t_ato_vinculoimovel_show_repository.execute(
            t_ato_vinculoimovel_id_schema
        )

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return response
