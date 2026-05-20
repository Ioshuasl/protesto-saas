from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_emolumento.g_emolumento_index_by_sistema_id_repository import (
    GEmolumentoIndexBySistemaIdRepository,
)
from packages.v1.administrativo.schemas.g_emolumento_schema import (
    GEmolumentoSistemaIdSchema,
)


class GEmolumentoIndexBySistemaIdAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a exibição
    de um registro na tabela G_NATUREZA_TITULO.
    """

    def execute(self, g_emolumento_sistema_id_schema: GEmolumentoSistemaIdSchema):
        """
        Executa a operação de exibição.

        Args:
            g_emolumento_id_schema (GEmolumentoIdSchema):
                O esquema com o ID do registro a ser exibido.

        Returns:
            O resultado da operação de exibição.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        g_emolumento_index_by_sistema_id_repository = (
            GEmolumentoIndexBySistemaIdRepository()
        )

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = g_emolumento_index_by_sistema_id_repository.execute(
            g_emolumento_sistema_id_schema
        )

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return response
