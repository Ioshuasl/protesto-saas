from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_tb_cartorio_schema import TTbCartorioSaveSchema
class TTbCartorioSaveRepository(BaseRepository):
    def execute(self, cartorio_schema: TTbCartorioSaveSchema):
        sql = """
            INSERT INTO T_TB_CARTORIO (
                TB_CARTORIO_ID,
                DESCRICAO,
                MUNICIPIO_ID,
                DESCRICAO_MUNICIPIO,
                CNS
            ) VALUES (
                :tb_cartorio_id,
                :descricao,
                :municipio_id,
                :descricao_municipio,
                :cns
            )
            RETURNING TB_CARTORIO_ID, DESCRICAO, MUNICIPIO_ID, DESCRICAO_MUNICIPIO, CNS
        """
        params = {
            "tb_cartorio_id": cartorio_schema.tb_cartorio_id,
            "descricao": cartorio_schema.descricao,
            "municipio_id": cartorio_schema.municipio_id,
            "descricao_municipio": cartorio_schema.descricao_municipio,
            "cns": cartorio_schema.cns,
        }
        return self.run_and_return(sql, params)
