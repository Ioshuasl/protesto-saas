from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_pessoa_schema import TPessoaEmailSchema


class TPessoaGetByEmailRepository(BaseRepository):
    def execute(self, t_pessoa_email_schema: TPessoaEmailSchema):
        sql = """
            SELECT TP.*, TPC.PESSOA_CARTAO_ID
            FROM T_PESSOA TP
            LEFT JOIN T_PESSOA_CARTAO TPC ON TP.PESSOA_ID = TPC.PESSOA_ID
            WHERE UPPER(TP.EMAIL) = UPPER(:email)
        """

        params = {"email": t_pessoa_email_schema.email.strip()}
        return self.fetch_one(sql, params)
