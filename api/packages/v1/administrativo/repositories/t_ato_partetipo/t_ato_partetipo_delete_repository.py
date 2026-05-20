from abstracts.repository import BaseRepository
from fastapi import HTTPException, status

from packages.v1.administrativo.schemas.t_ato_partetipo_schema import (
    TAtoParteTipoIdSchema,
)


class TAtoParteTipoDeleteRepository(BaseRepository):

    def execute(self, t_ato_partetipo_id_schema: TAtoParteTipoIdSchema):

        try:
            # Montagem do SQL
            sql = """
                DELETE FROM T_ATO_PARTETIPO TAP
                WHERE TAP.ATO_PARTETIPO_ID = :ato_partetipo_id
                RETURNING TAP.ATO_PARTETIPO_ID
            """

            # Parâmetros da query
            params = t_ato_partetipo_id_schema.model_dump(exclude_unset=True)

            # Execução da query
            response = self.run_and_return(sql, params)

            # Retorno do resultado
            return response

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir registro de T_IMOVEL: {str(e)}",
            )
