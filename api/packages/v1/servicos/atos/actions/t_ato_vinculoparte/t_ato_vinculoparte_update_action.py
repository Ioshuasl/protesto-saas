from abstracts.action import BaseAction
from packages.v1.servicos.atos.repositories.t_ato_vinculoparte.t_ato_vinculoparte_update_repository import (
    TAtoVinculoParteUpdateRepository,
)
from packages.v1.servicos.atos.schemas.t_ato_vinculoparte_schema import (
    TAtoVinculoParteUpdateSchema,
)


class TAtoVinculoParteUpdateAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a atualização
    de um registro na tabela G_NATUREZA_TITULO.
    """

    def execute(self, t_ato_vinculoparte_update_schema: TAtoVinculoParteUpdateSchema):
        """
        Executa a operação de atualização.

        Args:
            t_ato_vinculoparte_update_schema (TAtoVinculoParteUpdateSchema):
                O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório de atualização
        # ----------------------------------------------------
        t_ato_vinculoparte_update_repository = TAtoVinculoParteUpdateRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = t_ato_vinculoparte_update_repository.execute(
            t_ato_vinculoparte_update_schema
        )

        # ----------------------------------------------------
        # Retorno do resultado
        # ----------------------------------------------------
        return response
