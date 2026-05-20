from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_pessoa_sinal_publico_schema import (
    TPessoaSinalPublicoIdSchema,
)


class TPessoaSinalPublicoShowRepository(BaseRepository):
    def execute(self, pessoa_sinal_publico_schema: TPessoaSinalPublicoIdSchema):
        sql = """
            SELECT
                PSP.PESSOA_SINALPUBLICO_ID,
                PSP.NOME,
                PSP.TB_SINALPUBLICO_ID,
                PSP.PESSOA_ID
            FROM T_PESSOA_SINALPUBLICO PSP
            WHERE PSP.PESSOA_SINALPUBLICO_ID = :pessoa_sinalpublico_id
        """

        params = {
            "pessoa_sinalpublico_id": pessoa_sinal_publico_schema.pessoa_sinalpublico_id
        }
        return self.fetch_one(sql, params)
