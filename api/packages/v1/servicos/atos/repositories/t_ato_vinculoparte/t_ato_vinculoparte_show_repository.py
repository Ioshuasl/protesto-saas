from abstracts.repository import BaseRepository
from fastapi import HTTPException, status

from packages.v1.servicos.atos.schemas.t_ato_vinculoparte_schema import (
    TAtoVinculoParteIdSchema,
)


class TAtoVinculoParteShowRepository(BaseRepository):
    """
    Repositório responsável pela operação de exibição de um registro
    na tabela T_ATO_VINCULOPARTE.
    """

    def execute(self, t_ato_vinculoparte_id_schema: TAtoVinculoParteIdSchema):
        """
        Busca um registro específico de T_ATO_VINCULOPARTE pelo ID.

        Args:
            t_ato_vinculoparte_id_schema (TAtoVinculoParteIdSchema):
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
                FROM T_ATO_VINCULOPARTE GG
                WHERE GG.ATO_VINCULOPARTE_ID = :ato_vinculoparte_id
            """

            # ----------------------------------------------------
            # Preenchimento de parâmetros
            # ----------------------------------------------------
            params = t_ato_vinculoparte_id_schema.model_dump(exclude_unset=True)

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
                    detail="Registro de T_ATO_VINCULOPARTE não encontrado.",
                )

            return result

        except HTTPException:
            # Repassa exceções HTTP explícitas (como 404)
            raise

        except Exception as e:
            # Captura falhas inesperadas de execução
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao buscar registro em T_ATO_VINCULOPARTE: {e}",
            )
