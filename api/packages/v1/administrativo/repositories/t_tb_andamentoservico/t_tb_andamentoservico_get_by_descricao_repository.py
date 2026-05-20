from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_tb_andamentoservico_schema import TTbAndamentoservicoDescricaoSchema

class GetByDescricaoRepository(BaseRepository):
    """
    Repositório para a operação de busca de um registro na tabela
    t_tb_andamentoservico por descrição.
    """

    def execute(self, andamentoservico_schema: TTbAndamentoservicoDescricaoSchema):
        """
        Executa a consulta SQL para buscar um registro pela descrição.

        Args:
            andamentoservico_schema (TTbAndamentoservicoDescricaoSchema): O esquema com a descrição a ser buscada.

        Returns:
            Um dicionário contendo os dados do registro ou None se não for encontrado.
        """
        # Montagem do SQL
        sql = """ SELECT * FROM T_TB_ANDAMENTOSERVICO WHERE DESCRICAO = :descricao """

        # Preenchimento de parâmetros
        params = {
            'descricao': andamentoservico_schema.descricao
        }

        # Execução do sql
        return self.fetch_one(sql, params)