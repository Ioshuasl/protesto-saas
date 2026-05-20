from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_emolumento_schema import (
    GEmolumentoSistemaIdSchema,
)


class GEmolumentoIndexBySistemaIdRepository(BaseRepository):
    """
    Repositório para a operação de listagem de todos os registros
    na tabela t_censec_qualidade.
    """

    def execute(self, g_emolumento_sistema_id: GEmolumentoSistemaIdSchema):
        """
        Executa a consulta SQL para buscar todos os registros.

        Returns:
            Uma lista de dicionários contendo os dados dos registros.
        """
        # Montagem do SQL
        sql = """ SELECT
                    GE.*
                  FROM G_EMOLUMENTO GE
            """

        # lista de condições
        where = []

        # Verifica se deve filtrar a pesquisa
        if getattr(g_emolumento_sistema_id, "sistema_id", None):

            where.append("GE.SISTEMA_ID = :sistema_id")

        # Verifica se deve filtrar a pesquisa
        if getattr(g_emolumento_sistema_id, "situacao", None):

            where.append("GE.SITUACAO LIKE :situacao")

        if where:

            sql += " WHERE " + " AND ".join(where)

        params = g_emolumento_sistema_id.model_dump(exclude_unset=True)

        # Execução do sql
        response = self.fetch_all(sql, params)

        # Retorna os dados localizados
        return response
