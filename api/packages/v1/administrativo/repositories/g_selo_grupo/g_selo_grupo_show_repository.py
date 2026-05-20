from abstracts.repository import BaseRepository
from fastapi import HTTPException, status

from packages.v1.administrativo.schemas.g_selo_grupo_schema import GSeloGrupoIdSchema


class GSeloGrupoShowRepository(BaseRepository):
    """
    Repositório responsável pela operação de exibição de um registro
    na tabela G_SELO_GRUPO.
    """

    def execute(self, g_selo_grupo_id_schema: GSeloGrupoIdSchema):
        """
        Busca um registro específico de G_SELO_GRUPO pelo ID.

        Args:
            g_selo_grupo_id_schema (GSeloGrupoIdSchema):
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
                SELECT *
                FROM G_SELO_GRUPO GG
                WHERE GG.SELO_GRUPO_ID = :selo_grupo_id
            """

            # ----------------------------------------------------
            # Preenchimento de parâmetros
            # ----------------------------------------------------
            params = g_selo_grupo_id_schema.model_dump(exclude_unset=True)

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
                    detail="Registro de G_SELO_GRUPO não encontrado.",
                )

            return result

        except HTTPException:
            # Repassa exceções HTTP explícitas (como 404)
            raise

        except Exception as e:
            # Captura falhas inesperadas de execução
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao buscar registro em G_SELO_GRUPO: {e}",
            )
