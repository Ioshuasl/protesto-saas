from fastapi import HTTPException, status

from packages.v1.administrativo.actions.g_emolumento.g_emolumento_index_by_sistema_id_action import (
    GEmolumentoIndexBySistemaIdAction,
)
from packages.v1.administrativo.schemas.g_emolumento_schema import (
    GEmolumentoSistemaIdSchema,
)


class GEmolumentoIndexBySistemaIdService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de registros na tabela G_EMOLUMENTO.
    """

    def execute(self, g_emolumento_index_by_sistema_id: GEmolumentoSistemaIdSchema):
        """
        Executa a operação de busca de todos os registros no banco de dados.

        Args:
            g_emolumento_index_schema (GEmolumentoIndexSchema):
                Esquema que pode conter filtros ou parâmetros de busca.

        Returns:
            A lista de registros encontrados.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        g_emolumento_index_by_sistema_id_action = GEmolumentoIndexBySistemaIdAction()

        # ----------------------------------------------------
        # Execução da ação
        # ----------------------------------------------------
        data = g_emolumento_index_by_sistema_id_action.execute(
            g_emolumento_index_by_sistema_id
        )

        # ----------------------------------------------------
        # Verificação de retorno
        # ----------------------------------------------------
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar registros de G_EMOLUMENTO.",
            )

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return data
