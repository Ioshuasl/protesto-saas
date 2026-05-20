from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_tb_documentotipo_schema import GTbDocumentoTipoDescricaoSchema

class GetByDescricaoRepository(BaseRepository):
    """
    Repositório para a operação de busca de um registro na tabela
    g_tb_documentotipo por descrição.
    """

    def execute(self, documento_tipo_schema: GTbDocumentoTipoDescricaoSchema):
        """
        Executa a consulta SQL para buscar um registro pela descrição.

        Args:
            documento_tipo_schema (GTbDocumentoTipoDescricaoSchema): O esquema com a descrição a ser buscada.

        Returns:
            Um dicionário contendo os dados do registro ou None se não for encontrado.
        """
        # Montagem do SQL
        sql = """ SELECT TB_DOCUMENTOTIPO_ID,
                         DESCRICAO,
                         SITUACAO,
                         POSSUI_NUMERACAO,
                         ORGAO_PADRAO,
                         DESCRICAO_SIMPLIFICADA,
                         TIPO,
                         DESCRICAO_SINTER 
                  FROM G_TB_DOCUMENTOTIPO WHERE DESCRICAO = :descricao """

        # Preenchimento de parâmetros
        params = {
            'descricao': documento_tipo_schema.descricao
        }

        # Execução do sql
        return self.fetch_one(sql, params)