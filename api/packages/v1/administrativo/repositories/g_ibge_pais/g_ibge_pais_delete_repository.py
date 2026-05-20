from abstracts.repository import BaseRepository
from fastapi import HTTPException, status

from packages.v1.administrativo.schemas.g_ibge_pais_schema import (
    GIbgePaisIdSchema,
)


class GIbgePaisDeleteRepository(BaseRepository):
    """
    Repositório responsável pela exclusão de registros na tabela
    G_IBGE_PAIS.
    """

    def execute(self, g_ibge_pais_id_schema: GIbgePaisIdSchema):
        """
        Executa a exclusão de um registro específico da tabela G_IBGE_PAIS
        com base no ID informado.

        Args:
            g_ibge_pais_id_schema (GIbgePaisIdSchema):
                Esquema contendo o ID do registro a ser excluído.

        Returns:
            O resultado da operação de exclusão.
        """
        try:
            # Montagem do SQL
            sql = """
                DELETE FROM G_IBGE_PAIS
                 WHERE G_IBGE_PAIS_ID = :g_ibge_pais_id
            """

            # Preenchimento dos parâmetros
            params = {"g_ibge_pais_id": g_ibge_pais_id_schema.g_ibge_pais_id}

            # Execução da instrução SQL
            response = self.run(sql, params)

            # Retorna o resultado da exclusão
            return response

        except Exception as e:
            # Lança exceção HTTP em caso de erro
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir registro de G_IBGE_PAIS: {e}",
            )
