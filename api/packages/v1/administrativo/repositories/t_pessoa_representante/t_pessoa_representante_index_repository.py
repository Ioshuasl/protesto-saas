from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_pessoa_representante_schema import (
    TPessoaRepresentantePessoaIdSchema,
)


class TPessoaRepresentanteIndexRepository(BaseRepository):
    """
    Repositório para a operação de listagem de todos os registros
    na tabela g_tb_regimebens.
    """

    def execute(
        self,
        t_pessoa_representante_pessoa_id_schema: TPessoaRepresentantePessoaIdSchema,
    ):
        """
        Executa a consulta SQL para buscar todos os registros.

        Returns:
            Uma lista de dicionários contendo os dados dos registros.
        """
        # Montagem do SQL
        sql = """ SELECT
                    TPR.PESSOA_ID,
                    TPR.REPRESENTANTE_ID,
                    TPR.PESSOA_REPRESENTANTE_ID,
                    TPF.NOME,
                    TPF.CPF_CNPJ,
                    TPF.DATA_NASCIMENTO,
                    TPF.SEXO,
                    TPF.NACIONALIDADE,
                    TPF.NATURALIDADE,
                    TPF.EMAIL,
                    TPF.TELEFONE,
                    TPF.ENDERECO,
                    TPF.NUMERO_END,
                    TPF.BAIRRO,
                    TPF.CIDADE,
                    TPF.UF,
                    TPF.CEP,
                    TPF.pessoa_tipo
                FROM
                    T_PESSOA_REPRESENTANTE TPR
                JOIN T_PESSOA TPF ON
                    TPR.REPRESENTANTE_ID = TPF.PESSOA_ID
                JOIN T_PESSOA TPJ ON
                    TPR.PESSOA_ID = TPJ.PESSOA_ID
                WHERE TPR.PESSOA_ID = :pessoa_id"""

        params = {"pessoa_id": t_pessoa_representante_pessoa_id_schema.pessoa_id}

        # Execução do sql
        response = self.fetch_all(sql, params)

        # Retorna os dados localizados
        return response
