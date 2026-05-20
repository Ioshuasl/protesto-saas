from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_natureza_schema import (
    GNaturezaSistemaIdSchema,
)


class IndexBySistemaIdRepository(BaseRepository):
    """
    Repositório para a operação de listagem de todos os registros
    na tabela g_natureza.
    """

    def execute(self, g_natureza_sistema_id_schema: GNaturezaSistemaIdSchema):
        """
        Executa a consulta SQL para buscar todos os registros.

        Returns:
            Uma lista de dicionários contendo os dados dos registros.
        """
        # Montagem do SQL
        sql = """ SELECT * FROM G_NATUREZA WHERE sistema_id = :sistema_id"""

        # Montagem de parÂmetros
        params = {"sistema_id": g_natureza_sistema_id_schema.sistema_id}

        # Execução do sql
        response = self.fetch_all(sql, params)

        # Retorna os dados localizados
        return response
