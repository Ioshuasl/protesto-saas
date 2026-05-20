from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_tb_reconhecimentotipo_schema import TTbReconhecimentotipoDescricaoSchema

class GetByDescricaoRepository(BaseRepository):
    """
    Repositório para a operação de busca de um registro na tabela
    t_tb_reconhecimentotipo por descrição.
    """

    def execute(self, reconhecimentotipo_schema: TTbReconhecimentotipoDescricaoSchema):
        """
        Executa a consulta SQL para buscar um registro pela descrição.

        Args:
            reconhecimentotipo_schema (T_TbReconhecimentotipoDescricaoSchema): O esquema com a descrição a ser buscada.

        Returns:
            Um dicionário contendo os dados do registro ou None se não for encontrado.
        """
        # Montagem do SQL
        sql = """ SELECT * FROM T_TB_RECONHECIMENTOTIPO WHERE DESCRICAO = :descricao """

        # Preenchimento de parâmetros
        params = {
            'descricao': reconhecimentotipo_schema.descricao
        }

        # Execução do sql
        return self.fetch_one(sql, params)
