from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_pessoa_sinal_publico_schema import (
    TPessoaSinalPublicoIdSchema,
)


class TPessoaSinalPublicoDeleteRepository(BaseRepository):
    def execute(self, pessoa_sinal_publico_schema: TPessoaSinalPublicoIdSchema):
        try:
            sql = """
                DELETE FROM T_PESSOA_SINALPUBLICO
                WHERE PESSOA_SINALPUBLICO_ID = :pessoa_sinalpublico_id
                RETURNING PESSOA_SINALPUBLICO_ID
            """
            params = {
                "pessoa_sinalpublico_id": pessoa_sinal_publico_schema.pessoa_sinalpublico_id
            }
            return self.run_and_return(sql, params)
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir T_PESSOA_SINALPUBLICO: {exc}",
            )
