from abstracts.repository import BaseRepository
from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoProtocolarUpdateSchema


class TAtoProtocolarUpdateRepository(BaseRepository):
    def execute(self, data: TAtoProtocolarUpdateSchema):
        sql = """
            UPDATE T_ATO
            SET PROTOCOLO = :protocolo,
                DATA_PROTOCOLO = CURRENT_TIMESTAMP
            WHERE ATO_ID = :ato_id
              AND PROTOCOLO IS NULL
            RETURNING ATO_ID AS ato_id,
                      PROTOCOLO AS protocolo,
                      DATA_PROTOCOLO AS data_protocolo
        """
        return self.run_and_return(
            sql,
            {"protocolo": data.protocolo, "ato_id": data.ato_id},
        )
