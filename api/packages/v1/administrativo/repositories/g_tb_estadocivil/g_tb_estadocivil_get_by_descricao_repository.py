from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_tb_estadocivil_schema import GTbEstadoCivilDescricaoSchema

class GetByDescricaoRepository(BaseRepository):
    """
    Repositório para a operação de busca de um registro na tabela
    g_tb_estadocivil por descrição.
    """

    def execute(self, estadocivil_schema: GTbEstadoCivilDescricaoSchema):
        """
        Executa a consulta SQL para buscar um registro pela descrição.

        Args:
            estadocivil_schema (GTbEstadoCivilDescricaoSchema): O esquema com a descrição a ser buscada.

        Returns:
            Um dicionário contendo os dados do registro ou None se não for encontrado.
        """
        # Montagem do SQL
        sql = """ SELECT * FROM G_TB_ESTADOCIVIL WHERE DESCRICAO = :descricao """

        # Preenchimento de parâmetros
        params = {
            'descricao': estadocivil_schema.descricao
        }

        # Execução do sql
        return self.fetch_one(sql, params)