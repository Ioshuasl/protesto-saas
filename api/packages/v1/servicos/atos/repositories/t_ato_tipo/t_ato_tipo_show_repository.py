from abstracts.repository import BaseRepository
from fastapi import HTTPException, status

from packages.v1.servicos.atos.schemas.t_ato_tipo_schema import (
    TAtoTipoIdSchema,
)


class TAtoTipoShowRepository(BaseRepository):
    """
    Repositório responsável pela operação de exibição de um registro
    na tabela T_ATO_TIPO.
    """

    def execute(self, t_ato_tipo_id_schema: TAtoTipoIdSchema):
        """
        Busca um registro específico de T_ATO_TIPO pelo ID.

        Args:
            t_ato_tipo_id_schema (TAtoTipoIdSchema):
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
                        TAT.*,
                        TCT.POSSUI_ATO_ANTERIOR,
                        TCT.SITUACAO_ATO_ANTERIOR
                    FROM T_ATO_TIPO TAT
                    JOIN T_CENSEC_TIPONATUREZA TCT ON TAT.CENSEC_TIPONATUREZA_ID = TCT.CENSEC_TIPONATUREZA_ID
                    WHERE TAT.ATO_TIPO_ID = :ato_tipo_id
                """

            # ----------------------------------------------------
            # Preenchimento de parâmetros
            # ----------------------------------------------------
            params = t_ato_tipo_id_schema.model_dump(exclude_unset=True)

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
                    detail="Registro de T_ATO_TIPO não encontrado.",
                )

            return result

        except HTTPException:
            # Repassa exceções HTTP explícitas (como 404)
            raise

        except Exception as e:
            # Captura falhas inesperadas de execução
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao buscar registro em T_ATO_TIPO: {e}",
            )
