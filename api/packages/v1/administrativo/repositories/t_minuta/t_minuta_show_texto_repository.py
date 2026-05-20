from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_minuta_schema import TMinutaIdSchema
from fastapi import HTTPException, status

class TMinutaShowTextoRepository(BaseRepository):
    """
    Repositório para a operação de exibição de um registro na tabela t_minuta.
    """

    def execute(self, minuta_schema: TMinutaIdSchema):
        """
        Busca um registro específico de MINUTA pelo ID.

        Args:
            minuta_schema (TMinutaIdSchema): O esquema que contém o ID do registro.

        Returns:
            O registro encontrado ou None se não existir.

        Raises:
            HTTPException: Caso ocorra um erro na execução da query.
        """
        # Montagem do SQL
        sql = "SELECT MINUTA_ID, TEXTO FROM T_MINUTA WHERE MINUTA_ID = :minuta_id"

        # Preenchimento de parâmetros
        params = {
            'minuta_id': minuta_schema.minuta_id
        }

        # Execução do SQL
        result = self.fetch_one(sql, params)

        return result