from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_minuta_schema import TMinutaDescricaoSchema

class GetByDescricaoRepository(BaseRepository):
    """
    Repositório para a operação de busca de um registro na tabela
    t_minuta por descrição.
    """

    def execute(self, minuta_schema: TMinutaDescricaoSchema):
        """
        Executa a consulta SQL para buscar um registro pela descrição.

        Args:
            minuta_schema (TMinutaDescricaoSchema): O esquema com a descrição a ser buscada.

        Returns:
            Um dicionário contendo os dados do registro ou None se não for encontrado.
        """
        # Montagem do SQL
        sql = """ SELECT MINUTA_ID,
                         ATO_TIPO_ID,
                         NATUREZA_ID,
                         DESCRICAO,
                         PROTEGIDA,
                         SITUACAO 
                  FROM T_MINUTA WHERE DESCRICAO = :descricao """

        # Preenchimento de parâmetros
        params = {
            'descricao': minuta_schema.descricao
        }

        # Execução do sql
        return self.fetch_one(sql, params)