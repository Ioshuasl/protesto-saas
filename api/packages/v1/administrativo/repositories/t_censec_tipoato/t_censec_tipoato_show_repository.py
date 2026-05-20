from abstracts.repository import BaseRepository
from fastapi import HTTPException, status

from packages.v1.administrativo.schemas.t_censec_tipoato_schema import (
    TCensecTipoAtoIdSchema,
)


class TCensecTipoAtoShowRepository(BaseRepository):
    """
    Repositório responsável pela operação de exibição de um registro
    na tabela T_CENSEC_TIPOATO.
    """

    def execute(self, t_censec_tipoato_id_schema: TCensecTipoAtoIdSchema):
        """
        Busca um registro específico de T_CENSEC_TIPOATO pelo ID.

        Args:
            t_censec_tipoato_id_schema (TCensecTipoAtoIdSchema):
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
                FROM T_CENSEC_TIPOATO CTA
                WHERE CTA.CENSEC_TIPOATO_ID = :censec_tipoato_id
            """

            # ----------------------------------------------------
            # Preenchimento de parâmetros
            # ----------------------------------------------------
            params = {"censec_tipoato_id": t_censec_tipoato_id_schema.censec_tipoato_id}

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
                    detail="Registro de T_CENSEC_TIPOATO não encontrado.",
                )

            return result

        except HTTPException:
            # Repassa exceções HTTP explícitas (como 404)
            raise

        except Exception as e:
            # Captura falhas inesperadas de execução
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao buscar registro em T_CENSEC_TIPOATO: {e}",
            )
