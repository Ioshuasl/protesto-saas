from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_emolumento_item_schema import (
    GEmolumentoItemIndexSchema,
)


class GEmolumentoItemIndexRepository(BaseRepository):
    """
    Repositório para a operação de listagem de todos os registros
    na tabela t_censec_qualidade.
    """

    def execute(
        self, g_emolumento_item_emolumento_index_schema: GEmolumentoItemIndexSchema
    ):
        """
        Executa a consulta SQL para buscar todos os registros.

        Returns:
            Uma lista de dicionários contendo os dados dos registros.
        """
        # Montagem do SQL
        sql = """ SELECT
                    GI.*,
                    GSG.NUMERO
                FROM G_EMOLUMENTO_ITEM GI
                JOIN G_SELO_GRUPO gsg ON GI.SELO_GRUPO_ID = GSG.SELO_GRUPO_ID
                WHERE GI.EMOLUMENTO_ID = :emolumento_id
                AND GI.EMOLUMENTO_PERIODO_ID = :emolumento_periodo_id
            """

        # Preenchimento dos parâmetros
        params = {
            "emolumento_id": g_emolumento_item_emolumento_index_schema.emolumento_id,
            "emolumento_periodo_id": g_emolumento_item_emolumento_index_schema.emolumento_periodo_id,
        }

        # Execução do sql
        response = self.fetch_all(sql, params)

        # Retorna os dados localizados
        return response
