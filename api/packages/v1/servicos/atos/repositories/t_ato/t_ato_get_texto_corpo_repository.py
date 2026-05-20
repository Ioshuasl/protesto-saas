from abstracts.repository import BaseRepository
from fastapi import HTTPException, status

from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoIdSchema


class TAtoGetTextoCorpoRepository(BaseRepository):
    """
    Repositório responsável pela operação de exibição de um registro
    na tabela T_ATO.
    """

    def execute(self, data: TAtoIdSchema):

        # ----------------------------------------------------
        # Montagem do SQL
        # ----------------------------------------------------
        sql = """
            SELECT
                TA.ATO_ID,
                TLN.LIVRO_NATUREZA_ID,
                TA.TEXTO
            FROM T_ATO TA
            JOIN T_ATO_TIPO TAT ON TA.ATO_TIPO_ID = TAT.ATO_TIPO_ID
            JOIN T_LIVRO_NATUREZA TLN ON TAT.LIVRO_NATUREZA_ID = TLN.LIVRO_NATUREZA_ID
            WHERE TA.ATO_ID = :ato_id
        """

        # ----------------------------------------------------
        # Preenchimento de parâmetros
        # ----------------------------------------------------
        params = data.model_dump(exclude_unset=True)

        # ----------------------------------------------------
        # Execução do SQL
        # ----------------------------------------------------
        result = self.fetch_one(sql, params)

        return result
