from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from packages.v1.nfse.schemas.parametros_schema import ParametrosIdSchema


class ParametrosDeleteRepository(BaseRepository):
    def execute(self, data: ParametrosIdSchema):
        try:
            sql = """
                DELETE FROM PARAMETROS
                WHERE ID_PARAMETROS = :id_parametros
                RETURNING ID_PARAMETROS
            """
            return self.run_and_return(sql, {"id_parametros": data.id_parametros})
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir PARAMETROS: {exc}",
            )

