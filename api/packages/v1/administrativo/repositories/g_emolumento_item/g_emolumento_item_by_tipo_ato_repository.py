from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_emolumento_item_schema import (
    GEmolumentoItemByTipoAtoSchema,
)


class GEmolumentoItemByTipoAtoRepository(BaseRepository):
    """
    Repositório para a operação de listagem de todos os registros
    na tabela t_censec_qualidade.
    """

    def execute(self, data: GEmolumentoItemByTipoAtoSchema):
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
                    WHERE GI.EMOLUMENTO_PERIODO_ID = :emolumento_periodo_id
                    AND GSG.NUMERO = :numero
                 """

        # Preenchimento dos parâmetros
        params = {
            "emolumento_periodo_id": data.emolumento_periodo_id,
            "numero": data.numero,
        }

        # Execução do sql
        response = self.fetch_one(sql, params)

        # Retorna os dados localizados
        return response
