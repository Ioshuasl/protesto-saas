from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_tb_sinal_publico_schema import (
    TTbSinalPublicoUpdateSchema,
)


class TTbSinalPublicoUpdateRepository(BaseRepository):
    def execute(
        self,
        tb_sinalpublico_id: int,
        sinal_publico_schema: TTbSinalPublicoUpdateSchema,
    ):
        try:
            sql = """
                UPDATE T_TB_SINALPUBLICO
                SET DESCRICAO = :descricao,
                    SITUACAO = :situacao
                WHERE TB_SINALPUBLICO_ID = :tb_sinalpublico_id
                RETURNING TB_SINALPUBLICO_ID, DESCRICAO, SITUACAO
            """

            params = {
                "tb_sinalpublico_id": tb_sinalpublico_id,
                "descricao": sinal_publico_schema.descricao,
                "situacao": sinal_publico_schema.situacao,
            }

            return self.run_and_return(sql, params)
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar registro: {exc}",
            )
