from packages.v1.administrativo.actions.g_natureza_titulo.g_natureza_titulo_index_action import (
    GNaturezaTituloIndexAction,
)
from fastapi import HTTPException, status

from packages.v1.administrativo.schemas.g_natureza_titulo_schema import (
    GNaturezaTituloIndexSchema,
)


class GNaturezaTituloIndexService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de registros na tabela G_NATUREZA_TITULO.
    """

    def execute(self, g_natureza_titulo_index_schema: GNaturezaTituloIndexSchema):
        """
        Executa a operação de busca de todos os registros no banco de dados.

        Args:
            g_natureza_titulo_index_schema (GNaturezaTituloIndexSchema):
                Esquema que pode conter filtros ou parâmetros de busca.

        Returns:
            A lista de registros encontrados.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        g_natureza_titulo_index_action = GNaturezaTituloIndexAction()

        # ----------------------------------------------------
        # Execução da ação
        # ----------------------------------------------------
        data = g_natureza_titulo_index_action.execute(g_natureza_titulo_index_schema)

        # ----------------------------------------------------
        # Verificação de retorno
        # ----------------------------------------------------
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar registros de G_NATUREZA_TITULO.",
            )

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return data
