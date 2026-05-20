from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_tb_sinal_publico_schema import (
    TTbSinalPublicoIdSchema,
)


class TTbSinalPublicoDeleteRepository(BaseRepository):
    def execute(self, sinal_publico_schema: TTbSinalPublicoIdSchema):
        try:
            sql = """
                DELETE FROM T_TB_SINALPUBLICO
                WHERE TB_SINALPUBLICO_ID = :tb_sinalpublico_id
                RETURNING TB_SINALPUBLICO_ID
            """

            params = {"tb_sinalpublico_id": sinal_publico_schema.tb_sinalpublico_id}
            return self.run_and_return(sql, params)
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir T_TB_SINALPUBLICO: {exc}",
            )
