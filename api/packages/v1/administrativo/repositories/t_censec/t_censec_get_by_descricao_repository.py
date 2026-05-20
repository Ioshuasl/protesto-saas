from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_censec_schema import TCensecDescricaoSchema

class GetByDescricaoRepository(BaseRepository):
    """
    Repositório para a operação de busca de um registro na tabela
    t_censec por descrição.
    """

    def execute(self, censec_schema: TCensecDescricaoSchema):
        """
        Executa a consulta SQL para buscar um registro pela descrição.

        Args:
            censec_schema (TCensecDescricaoSchema): O esquema com a descrição a ser buscada.

        Returns:
            Um dicionário contendo os dados do registro ou None se não for encontrado.
        """
        # Montagem do SQL
        sql = """ SELECT * FROM T_CENSEC WHERE DESCRICAO = :descricao """

        # Preenchimento de parâmetros
        params = {
            'descricao': censec_schema.descricao
        }

        # Execução do sql
        return self.fetch_one(sql, params)