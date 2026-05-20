from abstracts.action import BaseAction
from packages.v1.servicos.atos.repositories.t_ato_vinculoparte.t_ato_vinculoparte_show_repository import (
    TAtoVinculoParteShowRepository,
)
from packages.v1.servicos.atos.schemas.t_ato_vinculoparte_schema import (
    TAtoVinculoParteIdSchema,
)


class TAtoVinculoParteShowAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a exibição
    de um registro na tabela G_NATUREZA_TITULO.
    """

    def execute(self, t_ato_vinculoparte_id_schema: TAtoVinculoParteIdSchema):
        """
        Executa a operação de exibição.

        Args:
            t_ato_vinculoparte_id_schema (TAtoVinculoParteIdSchema):
                O esquema com o ID do registro a ser exibido.

        Returns:
            O resultado da operação de exibição.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        t_ato_vinculoparte_show_repository = TAtoVinculoParteShowRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = t_ato_vinculoparte_show_repository.execute(
            t_ato_vinculoparte_id_schema
        )

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return response
