from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_biometria_pessoa_schema import (
    TBiometriaPessoaIndexSchema,
)


class TBiometriaPessoaIndexRepository(BaseRepository):
    """
    Repositório para a operação de listagem de todos os registros
    na tabela t_censec_qualidade.
    """

    def __init__(self):

        # Ativa conversão automática de BLOB para Base64
        super().__init__(blob_in_base64=True)

    def execute(self, biometria_pessoa_index_schema: TBiometriaPessoaIndexSchema):
        """
        Executa a consulta SQL para buscar todos os registros.

        Returns:
            Uma lista de dicionários contendo os dados dos registros.
        """
        # Montagem do SQL
        sql = """ SELECT
                    tbp.*
                  FROM T_BIOMETRIA_PESSOA TBP
                  WHERE TBP.CHAVE_ID = :chave_id
            """

        params = {"chave_id": biometria_pessoa_index_schema.chave_id}

        # Execução do sql
        response = self.fetch_all(sql, params)

        # Retorna os dados localizados
        return response
