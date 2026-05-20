from fastapi import HTTPException, status
from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_tb_regimecomunhao_schema import GTbRegimecomunhaoSaveSchema


class SaveRepository(BaseRepository):

    def execute(self, regimecomunhao_schema: GTbRegimecomunhaoSaveSchema):

        try:

            # Montagem do SQL
            sql = """ INSERT INTO G_TB_REGIMECOMUNHAO (
                        TB_REGIMECOMUNHAO_ID,
                        DESCRICAO,
                        TEXTO,
                        SITUACAO,
                        TB_REGIMEBENS_ID
                    ) VALUES (
                        :tb_regimecomunhao_id,
                        :descricao,
                        :texto,
                        :situacao,
                        :tb_regimebens_id
                    ) RETURNING *;"""

            # Preenchimento de parâmetros
            params = {
                'tb_regimecomunhao_id': regimecomunhao_schema.tb_regimecomunhao_id,
                'descricao': regimecomunhao_schema.descricao,
                'texto': regimecomunhao_schema.texto.encode("utf-8") if regimecomunhao_schema.texto else None, # Convertendo string para bytes
                'situacao': regimecomunhao_schema.situacao,
                'tb_regimebens_id': regimecomunhao_schema.tb_regimebens_id
            }

            # Execução do sql
            return self.run_and_return(sql, params)

        except Exception as e:

            # Informa que houve uma falha na atualização do usuário
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao salvar regime de comunhão: {e}"
            )