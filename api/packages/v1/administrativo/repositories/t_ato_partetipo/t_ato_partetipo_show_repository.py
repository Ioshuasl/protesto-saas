from abstracts.repository import BaseRepository
from fastapi import HTTPException, status

from packages.v1.administrativo.schemas.t_ato_partetipo_schema import (
    TAtoParteTipoIdSchema,
)


class TAtoParteTipoShowRepository(BaseRepository):
    """
    Repositório para a operação de exibição de um registro na tabela t_censec_qualidade.
    """

    def execute(self, t_ato_partetipo_id_schema: TAtoParteTipoIdSchema):
        """
        Busca um registro específico de CENSEC_QUALIDADE pelo ID.

        Args:
            t_ato_partetipo_schema (TAtoParteTipoIdSchema): O esquema que contém o ID do registro.

        Returns:
            O registro encontrado ou None se não existir.

        Raises:
            HTTPException: Caso ocorra um erro na execução da query.
        """
        try:
            # Montagem do SQL
            sql = "SELECT * FROM T_ATO_PARTETIPO TAP WHERE TAP.ATO_PARTETIPO_ID = :ato_partetipo_id"

            # ----------------------------------------------------
            # Preenchimento dos parâmetros de acordo com o schema
            # ----------------------------------------------------
            params = t_ato_partetipo_id_schema.model_dump(exclude_unset=True)

            # Execução do SQL
            result = self.fetch_one(sql, params)

            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Registro não encontrado",
                )

            return result
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao buscar registro: {str(e)}",
            )
