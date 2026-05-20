from abstracts.repository import BaseRepository
from fastapi import HTTPException, status

from packages.v1.servicos.atos.schemas.t_ato_vinculovalor_schema import (
    TAtoVinculoValorIdSchema,
)


class TAtoVinculoValorShowRepository(BaseRepository):
    """
    Repositório responsável pela operação de exibição de um registro
    na tabela T_ATO_VINCULOVALOR.
    """

    def execute(self, t_ato_vinculovalor_id_schema: TAtoVinculoValorIdSchema):
        """
        Busca um registro específico de T_ATO_VINCULOVALOR pelo ID.

        Args:
            t_ato_vinculovalor_id_schema (TAtoVinculoValorIdSchema):
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
                FROM T_ATO_VINCULOVALOR GG
                WHERE GG.ATO_VINCULOVALOR_ID = :ato_vinculovalor_id
            """

            # ----------------------------------------------------
            # Preenchimento de parâmetros
            # ----------------------------------------------------
            params = t_ato_vinculovalor_id_schema.model_dump(exclude_unset=True)

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
                    detail="Registro de T_ATO_VINCULOVALOR não encontrado.",
                )

            return result

        except HTTPException:
            # Repassa exceções HTTP explícitas (como 404)
            raise

        except Exception as e:
            # Captura falhas inesperadas de execução
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao buscar registro em T_ATO_VINCULOVALOR: {e}",
            )
