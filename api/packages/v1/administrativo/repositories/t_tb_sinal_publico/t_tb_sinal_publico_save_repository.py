from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_tb_sinal_publico_schema import (
    TTbSinalPublicoSaveSchema,
)


class TTbSinalPublicoSaveRepository(BaseRepository):
    def execute(self, sinal_publico_schema: TTbSinalPublicoSaveSchema):
        try:
            sql = """
                INSERT INTO T_TB_SINALPUBLICO (
                    TB_SINALPUBLICO_ID,
                    DESCRICAO,
                    SITUACAO
                ) VALUES (
                    :tb_sinalpublico_id,
                    :descricao,
                    :situacao
                )
                RETURNING TB_SINALPUBLICO_ID, DESCRICAO, SITUACAO
            """

            params = {
                "tb_sinalpublico_id": sinal_publico_schema.tb_sinalpublico_id,
                "descricao": sinal_publico_schema.descricao,
                "situacao": sinal_publico_schema.situacao,
            }

            return self.run_and_return(sql, params)
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao salvar registro: {exc}",
            )
