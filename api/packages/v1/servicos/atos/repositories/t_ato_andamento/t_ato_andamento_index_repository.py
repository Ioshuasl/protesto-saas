from abstracts.repository import BaseRepository
from packages.v1.servicos.atos.schemas.t_ato_andamento_schema import (
    TAtoAndamentoIndexSchema,
)


class TAtoAndamentoIndexRepository(BaseRepository):

    def execute(self, data: TAtoAndamentoIndexSchema):

        # Montagem do SQL
        sql = """
                SELECT
                    TAA.*,
                    GU.NOME_COMPLETO,
                    GU.FUNCAO,
                    TTAS.DESCRICAO
                FROM T_ATO_ANDAMENTO TAA
                LEFT JOIN G_USUARIO GU
                    ON GU.USUARIO_ID = TAA.USUARIO_ID
                LEFT JOIN T_TB_ANDAMENTOSERVICO TTAS
                    ON TTAS.TB_ANDAMENTOSERVICO_ID = TAA.TB_ANDAMENTOSERVICO_ID
                WHERE
                    TAA.ATO_ID = :ato_id
              """

        # ----------------------------------------------------
        # Preenchimento dos parâmetros
        # ----------------------------------------------------
        params = data.model_dump(exclude_unset=True)

        # Execução do sql
        response = self.fetch_all(sql, params)

        # Retorna os dados localizados
        return response
