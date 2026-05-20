from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_pessoa_sinal_publico_schema import (
    TPessoaSinalPublicoSchema,
)


class TPessoaSinalPublicoIndexRepository(BaseRepository):
    def execute(self, data: TPessoaSinalPublicoSchema):
        sql = """
            SELECT
                PSP.PESSOA_SINALPUBLICO_ID,
                PSP.NOME,
                PSP.TB_SINALPUBLICO_ID,
                PSP.PESSOA_ID
            FROM T_PESSOA_SINALPUBLICO PSP
            WHERE psp.pessoa_id = :pessoa_id
            ORDER BY PSP.PESSOA_SINALPUBLICO_ID
        """

        params = {"pessoa_id": data.pessoa_id}

        return self.fetch_all(sql, params)
