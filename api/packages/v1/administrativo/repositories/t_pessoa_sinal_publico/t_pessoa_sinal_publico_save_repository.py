from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_pessoa_sinal_publico_schema import (
    TPessoaSinalPublicoSaveSchema,
)


class TPessoaSinalPublicoSaveRepository(BaseRepository):
    def execute(self, pessoa_sinal_publico_schema: TPessoaSinalPublicoSaveSchema):
        try:
            sql = """
                INSERT INTO T_PESSOA_SINALPUBLICO (
                    PESSOA_SINALPUBLICO_ID,
                    NOME,
                    TB_SINALPUBLICO_ID,
                    PESSOA_ID
                ) VALUES (
                    :pessoa_sinalpublico_id,
                    :nome,
                    :tb_sinalpublico_id,
                    :pessoa_id
                )
                RETURNING PESSOA_SINALPUBLICO_ID, NOME, TB_SINALPUBLICO_ID, PESSOA_ID
            """

            params = {
                "pessoa_sinalpublico_id": pessoa_sinal_publico_schema.pessoa_sinalpublico_id,
                "nome": pessoa_sinal_publico_schema.nome,
                "tb_sinalpublico_id": pessoa_sinal_publico_schema.tb_sinalpublico_id,
                "pessoa_id": pessoa_sinal_publico_schema.pessoa_id,
            }

            return self.run_and_return(sql, params)
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao salvar registro: {exc}",
            )
