from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_cidade_schema import GCidadeIndexSchema


class IndexRepository(BaseRepository):
    """
    Repositório para a operação de listagem de todos os registros
    na tabela G_CIDADE.
    """

    def execute(self, data: GCidadeIndexSchema):
        """
        Executa a consulta SQL para buscar todos os registros.

        Returns:
            Uma lista de dicionários contendo os dados dos registros.
        """
        # Montagem do SQL
        sql = """ SELECT GC.CIDADE_ID,
                        GC.UF,
                        GC.CIDADE_NOME,
                        GC.CODIGO_IBGE,
                        GC.CODIGO_GYN
                    FROM G_CIDADE GC
                    WHERE GC.UF = :uf
                    ORDER BY CIDADE_NOME ASC"""

        params = {"uf": data.uf}

        # Execução do sql
        response = self.fetch_all(sql, params)

        # Retorna os dados localizados
        return response
