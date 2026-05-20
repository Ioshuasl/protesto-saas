from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_tb_txmodelogrupo_schema import GTbTxmodelogrupoUpdateSchema
from fastapi import HTTPException, status

class UpdateRepository(BaseRepository):

    def execute(self, tb_txmodelogrupo_id: int, txmodelogrupo_schema: GTbTxmodelogrupoUpdateSchema):
        try:
            updates = []
            params = {}

            if txmodelogrupo_schema.descricao is not None:
                updates.append("DESCRICAO = :descricao")
                params["descricao"] = txmodelogrupo_schema.descricao

            if txmodelogrupo_schema.situacao is not None:
                updates.append("SITUACAO = :situacao")
                params["situacao"] = txmodelogrupo_schema.situacao

            if txmodelogrupo_schema.sistema_id is not None:
                updates.append("SISTEMA_ID = :sistema_id")
                params["sistema_id"] = txmodelogrupo_schema.sistema_id

            if not updates:
                return False

            params["tb_txmodelogrupo_id"] = tb_txmodelogrupo_id
            sql = f"UPDATE G_TB_TXMODELOGRUPO SET {', '.join(updates)} WHERE tb_txmodelogrupo_id = :tb_txmodelogrupo_id RETURNING *;"

            # Executa a query
            result = self.run_and_return(sql, params)

            if not result or not hasattr(result, 'tb_txmodelogrupo_id') or result.tb_txmodelogrupo_id is None:
                # Informa que não existe o registro a ser modificado
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail='Nenhum registro de modelo de grupo localizado para esta solicitação'
                )

            # Verifica o resultado da execução
            if result:
                # Se houver um resultado, a atualização foi bem-sucedida
                return result

        except Exception as e:
            # Informa que houve uma falha na atualização
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar modelo de grupo: {e}"
            )