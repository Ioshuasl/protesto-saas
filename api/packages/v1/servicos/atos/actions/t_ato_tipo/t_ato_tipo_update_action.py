from abstracts.action import BaseAction
from packages.v1.servicos.atos.repositories.t_ato_tipo.t_ato_tipo_update_repository import (
    TAtoTipoUpdateRepository,
)
from packages.v1.servicos.atos.schemas.t_ato_tipo_schema import (
    TAtoTipoUpdateSchema,
)


class TAtoTipoUpdateAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a atualização
    de um registro na tabela G_NATUREZA_TITULO.
    """

    def execute(self, t_ato_tipo_update_schema: TAtoTipoUpdateSchema):
        """
        Executa a operação de atualização.

        Args:
            t_ato_tipo_update_schema (TAtoTipoUpdateSchema):
                O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório de atualização
        # ----------------------------------------------------
        t_ato_tipo_update_repository = TAtoTipoUpdateRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = t_ato_tipo_update_repository.execute(
            t_ato_tipo_update_schema
        )

        # ----------------------------------------------------
        # Retorno do resultado
        # ----------------------------------------------------
        return response
