import re

from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_pessoa_schema import TPessoaCpfSchema


class TPessoaGetByCpfRepository(BaseRepository):
    @staticmethod
    def limpar_cpf(cpf: str) -> str:
        return re.sub(r"\D", "", cpf or "")

    @staticmethod
    def aplicar_mascara_cpf(cpf: str) -> str:
        if len(cpf) == 11:
            return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
        return cpf

    def execute(self, t_pessoa_cpf_schema: TPessoaCpfSchema):
        cpf_limpo = self.limpar_cpf(t_pessoa_cpf_schema.cpf)
        cpf_mascarado = self.aplicar_mascara_cpf(cpf_limpo)

        sql = """
            SELECT TP.*, TPC.PESSOA_CARTAO_ID
            FROM T_PESSOA TP
            LEFT JOIN T_PESSOA_CARTAO TPC ON TP.PESSOA_ID = TPC.PESSOA_ID
            WHERE TP.CPF_CNPJ = :cpf_limpo
               OR TP.CPF_CNPJ = :cpf_mascarado
        """

        params = {"cpf_limpo": cpf_limpo, "cpf_mascarado": cpf_mascarado}
        return self.fetch_one(sql, params)
