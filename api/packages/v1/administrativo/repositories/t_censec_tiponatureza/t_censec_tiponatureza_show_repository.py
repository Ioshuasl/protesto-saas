from abstracts.repository import BaseRepository
from fastapi import HTTPException, status

from packages.v1.administrativo.schemas.t_censec_tiponatureza_schema import (
    TCensecTipoNaturezaIdSchema,
)


class TCensecTipoNaturezaShowRepository(BaseRepository):
    """
    Repositório responsável pela operação de exibição de um registro
    na tabela T_CENSEC_TIPONATUREZA.
    """

    def execute(self, t_censec_tiponatureza_id_schema: TCensecTipoNaturezaIdSchema):
        """
        Busca um registro específico de T_CENSEC_TIPONATUREZA pelo ID.

        Args:
            t_censec_tiponatureza_id_schema (TCensecTipoNaturezaIdSchema):
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
                FROM T_CENSEC_TIPONATUREZA TCT
                WHERE TCT.CENSEC_TIPONATUREZA_ID = :censec_tiponatureza_id
            """

            # ----------------------------------------------------
            # Preenchimento de parâmetros
            # ----------------------------------------------------
            params = t_censec_tiponatureza_id_schema.model_dump(exclude_unset=True)

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
                    detail="Registro de T_CENSEC_TIPONATUREZA não encontrado.",
                )

            return result

        except HTTPException:
            # Repassa exceções HTTP explícitas (como 404)
            raise

        except Exception as e:
            # Captura falhas inesperadas de execução
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao buscar registro em T_CENSEC_TIPONATUREZA: {e}",
            )
