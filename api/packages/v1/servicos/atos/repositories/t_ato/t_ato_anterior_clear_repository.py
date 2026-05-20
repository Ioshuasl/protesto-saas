from abstracts.repository import BaseRepository

from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoAnteriorClearSchema


class TAtoAnteriorClearRepository(BaseRepository):
    def execute(self, data: TAtoAnteriorClearSchema):
        sql = """
            UPDATE T_ATO
            SET
                ATO_ANTERIOR_ORIGEM = NULL,
                ATO_ANTERIOR_LIVRO = NULL,
                ATO_ANTERIOR_FINICIAL = NULL,
                ATO_ANTERIOR_TB_CARTORIO_ID = NULL,
                ATO_ANTERIOR_OUTORGANTE = NULL,
                ATO_ANTERIOR_OBSERVACAO = NULL,
                ATO_ANTERIOR_ATO_ID = NULL,
                ATO_ANTERIOR_DATA = NULL,
                ATO_ANTERIOR_ANOTACAO_ADICIONAL = NULL,
                ATO_ANTERIOR_ATO_TIPO_ID = NULL,
                ATO_ANTERIOR_VALOR_DOCUMENTO = NULL
            WHERE ATO_ID = :ato_id
            RETURNING *;
        """
        return self.run_and_return(sql, {"ato_id": data.ato_id})
