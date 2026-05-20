from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_natureza_titulo_schema import (
    GNaturezaTituloIndexSchema,
)


class GNaturezaTituloIndexRepository(BaseRepository):
    """
    Repositório para a operação de listagem de todos os registros
    na tabela t_censec_qualidade.
    """

    def execute(self, g_natureza_titulo_index_schema: GNaturezaTituloIndexSchema):
        """
        Executa a consulta SQL para buscar todos os registros.

        Returns:
            Uma lista de dicionários contendo os dados dos registros.
        """
        # Montagem do SQL
        sql = """ SELECT
                    GNT.*
                  FROM G_NATUREZA_TITULO GNT
                  WHERE GNT.SISTEMA_ID = :sistema_id
            """

        # Montagem dos parâmetros
        params = g_natureza_titulo_index_schema.model_dump(exclude_unset=True)

        # Execução do sql
        response = self.fetch_all(sql, params)

        # Retorna os dados localizados
        return response
