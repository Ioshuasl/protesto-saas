from abstracts.repository import BaseRepository
from fastapi import HTTPException, status

from packages.v1.administrativo.schemas.g_ibge_pais_schema import (
    GIbgePaisIdSchema,
)


class GIbgePaisShowRepository(BaseRepository):
    """
    Repositório responsável pela operação de exibição de um registro
    na tabela G_IBGE_PAIS.
    """

    def execute(self, g_ibge_pais_id_schema: GIbgePaisIdSchema):
        """
        Busca um registro específico de G_IBGE_PAIS pelo ID.

        Args:
            g_ibge_pais_id_schema (GIbgePaisIdSchema):
                Esquema contendo o ID do registro a ser buscado.

        Returns:
            O registro encontrado ou levanta exceção HTTP 404 se não existir.

        Raises:
            HTTPException: Caso ocorra um erro na execução da query.
        """
        try:
            # ----------------------------------------------------
            # Montagem do SQL
            # ----------------------------------------------------
            sql = """
                SELECT
                    T.*
                FROM G_IBGE_PAIS T
                WHERE T.G_IBGE_PAIS_ID = :g_ibge_pais_id
            """

            # ----------------------------------------------------
            # Preenchimento de parâmetros
            # ----------------------------------------------------
            params = g_ibge_pais_id_schema.model_dump(exclude_unset=True)

            # ----------------------------------------------------
            # Execução do SQL
            # ----------------------------------------------------
            result = self.fetch_one(sql, params)

            # ----------------------------------------------------
            # Validação de retorno
            # ----------------------------------------------------
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Registro de G_IBGE_PAIS não encontrado.",
                )

            return result

        except HTTPException:
            # Repassa exceções HTTP explícitas (como 404)
            raise

        except Exception as e:
            # Captura falhas inesperadas de execução
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao buscar registro em G_IBGE_PAIS: {e}",
            )
