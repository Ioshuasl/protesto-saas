from abstracts.repository import BaseRepository
from fastapi import HTTPException, status

from packages.v1.administrativo.schemas.g_emolumento_schema import GEmolumentoIdSchema


class GEmolumentoShowRepository(BaseRepository):
    """
    Repositório responsável pela operação de exibição de um registro
    na tabela G_EMOLUMENTO.
    """

    def execute(self, g_emolumento_id_schema: GEmolumentoIdSchema):
        """
        Busca um registro específico de G_EMOLUMENTO pelo ID.

        Args:
            g_emolumento_id_schema (GEmolumentoIdSchema):
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
                FROM G_EMOLUMENTO GG
                WHERE GG.EMOLUMENTO_ID = :emolumento_id
            """

            # ----------------------------------------------------
            # Preenchimento de parâmetros
            # ----------------------------------------------------
            params = g_emolumento_id_schema.model_dump(exclude_unset=True)

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
                    detail="Registro de G_EMOLUMENTO não encontrado.",
                )

            return result

        except HTTPException:
            # Repassa exceções HTTP explícitas (como 404)
            raise

        except Exception as e:
            # Captura falhas inesperadas de execução
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao buscar registro em G_EMOLUMENTO: {e}",
            )
