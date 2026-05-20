from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_pessoa_sinal_publico_schema import (
    TPessoaSinalPublicoUpdateSchema,
)


class TPessoaSinalPublicoUpdateRepository(BaseRepository):
    def execute(
        self,
        pessoa_sinalpublico_id: int,
        pessoa_sinal_publico_schema: TPessoaSinalPublicoUpdateSchema,
    ):
        try:
            sql = """
                UPDATE T_PESSOA_SINALPUBLICO
                SET NOME = :nome,
                    TB_SINALPUBLICO_ID = :tb_sinalpublico_id,
                    PESSOA_ID = :pessoa_id
                WHERE PESSOA_SINALPUBLICO_ID = :pessoa_sinalpublico_id
                RETURNING PESSOA_SINALPUBLICO_ID, NOME, TB_SINALPUBLICO_ID, PESSOA_ID
            """

            params = {
                "pessoa_sinalpublico_id": pessoa_sinalpublico_id,
                "nome": pessoa_sinal_publico_schema.nome,
                "tb_sinalpublico_id": pessoa_sinal_publico_schema.tb_sinalpublico_id,
                "pessoa_id": pessoa_sinal_publico_schema.pessoa_id,
            }

            return self.run_and_return(sql, params)
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar registro: {exc}",
            )
