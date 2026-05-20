from fastapi import HTTPException, status
from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_tb_txmodelogrupo_schema import GTbTxmodelogrupoSaveSchema


class SaveRepository(BaseRepository):

    def execute(self, txmodelogrupo_schema: GTbTxmodelogrupoSaveSchema):
        try:
            # Montagem do SQL
            sql = """
                INSERT INTO G_TB_TXMODELOGRUPO (
                    TB_TXMODELOGRUPO_ID,
                    DESCRICAO,
                    SITUACAO,
                    SISTEMA_ID
                ) VALUES (
                    :tb_txmodelogrupo_id,
                    :descricao,
                    :situacao,
                    :sistema_id
                ) RETURNING *;
            """

            # Preenchimento de parâmetros
            params = {
                'tb_txmodelogrupo_id': txmodelogrupo_schema.tb_txmodelogrupo_id,
                'descricao': txmodelogrupo_schema.descricao,
                'situacao': txmodelogrupo_schema.situacao,
                'sistema_id': txmodelogrupo_schema.sistema_id
            }

            # Execução do SQL
            return self.run_and_return(sql, params)

        except Exception as e:
            # Informa que houve uma falha ao salvar o registro
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao salvar modelo de grupo: {e}"
            )