from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoLavraturaSchema


class TAtoLavrarAtoRepository(BaseRepository):
    """
    Marca o ato como lavrado (SITUACAO_ATO = 3), registrando
    DATA_LAVRATURA e USUARIO_ID_LAVRATURA.
    """

    def execute(self, data: TAtoLavraturaSchema, connection=None):
        sql = """
            UPDATE T_ATO
            SET SITUACAO_ATO = :situacao_ato,
                DATA_LAVRATURA = CURRENT_TIMESTAMP,
                USUARIO_ID_LAVRATURA = :usuario_id,
                FOLHA_INICIAL = :folha_inicial,
                FOLHA_FINAL = :folha_final,
                FOLHA_TOTAL = :folha_total,
                LIVRO_ANDAMENTO_ID = :livro_andamento_id,
                SELO_LIVRO_ID = :selo_livro_id
            WHERE ATO_ID = :ato_id
            RETURNING ATO_ID AS ato_id
        """
        params = {
            "ato_id": data.ato_id,
            "usuario_id": data.usuario_id,
            "situacao_ato": data.situacao_ato,
            "folha_inicial": data.folha_inicial,
            "folha_final": data.folha_final,
            "folha_total": data.folha_total,
            "livro_andamento_id": data.livro_andamento_id,
            "selo_livro_id": data.selo_livro_id,
        }
        return self.run_and_return(sql, params, connection=connection)
