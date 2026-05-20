from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_emolumento.g_emolumento_update_repository import (
    GEmolumentoUpdateRepository,
)
from packages.v1.administrativo.schemas.g_emolumento_schema import (
    GEmolumentoUpdateSchema,
)


class GEmolumentoUpdateAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a atualização
    de um registro na tabela G_NATUREZA_TITULO.
    """

    def execute(self, g_emolumento_update_schema: GEmolumentoUpdateSchema):
        """
        Executa a operação de atualização.

        Args:
            g_emolumento_update_schema (GEmolumentoUpdateSchema):
                O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório de atualização
        # ----------------------------------------------------
        g_emolumento_update_repository = GEmolumentoUpdateRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = g_emolumento_update_repository.execute(g_emolumento_update_schema)

        # ----------------------------------------------------
        # Retorno do resultado
        # ----------------------------------------------------
        return response
