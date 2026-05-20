from packages.v1.administrativo.actions.g_ibge_pais.g_ibge_pais_show_action import (
    GIbgePaisShowAction,
)
from packages.v1.administrativo.schemas.g_ibge_pais_schema import (
    GIbgePaisIdSchema,
)
from fastapi import HTTPException, status


class GIbgePaisShowService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela {{ entity_upper }}.
    """

    def execute(self, g_ibge_pais_id_schema: GIbgePaisIdSchema):
        """
        Executa a operação de busca no banco de dados.

        Args:
            g_ibge_pais_id_schema (GIbgePaisIdSchema):
                O esquema com o ID do registro a ser buscado.

        Returns:
            O resultado da busca.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        g_ibge_pais_show_action = GIbgePaisShowAction()

        # ----------------------------------------------------
        # Execução da ação
        # ----------------------------------------------------
        data = g_ibge_pais_show_action.execute(g_ibge_pais_id_schema)

        # ----------------------------------------------------
        # Verificação de resultado
        # ----------------------------------------------------
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar o registro de {{ entity_upper }}.",
            )

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return data
