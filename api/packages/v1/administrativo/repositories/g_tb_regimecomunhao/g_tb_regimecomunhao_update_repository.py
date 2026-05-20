from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_tb_regimecomunhao_schema import GTbRegimecomunhaoUpdateSchema
from fastapi import HTTPException, status

class UpdateRepository(BaseRepository):

    def execute(self, tb_regimecomunhao_id : int, regimecomunhao_schema: GTbRegimecomunhaoUpdateSchema):

        try:
            updates = []
            params = {}

            if regimecomunhao_schema.descricao is not None:
                updates.append("DESCRICAO = :descricao")
                params["descricao"] = regimecomunhao_schema.descricao

            if regimecomunhao_schema.texto is not None:
                updates.append("TEXTO = :texto")
                params["texto"] = (
                    regimecomunhao_schema.texto.encode("utf-8")
                    if isinstance(regimecomunhao_schema.texto, str)
                    else regimecomunhao_schema.texto
                )

            if regimecomunhao_schema.situacao is not None:
                updates.append("SITUACAO = :situacao")
                params["situacao"] = regimecomunhao_schema.situacao

            if regimecomunhao_schema.tb_regimebens_id is not None:
                updates.append("TB_REGIMEBENS_ID = :tb_regimebens_id")
                params["tb_regimebens_id"] = regimecomunhao_schema.tb_regimebens_id

            if not updates:
                return False

            params["tb_regimecomunhao_id"] = tb_regimecomunhao_id
            sql = f"UPDATE G_TB_REGIMECOMUNHAO SET {', '.join(updates)} WHERE tb_regimecomunhao_id = :tb_regimecomunhao_id RETURNING *;"

            # Executa a query
            result = self.run_and_return(sql, params)

            if not result.tb_regimecomunhao_id:

                # Informa que não existe o registro a ser modificado
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail='Nenhum regime de comunhão localizado para esta solicitação'
                )

            # Verifica o resultado da execução
            if result:
                # Se houver um resultado, a atualização foi bem-sucedida
                return result


        except Exception as e:

            # Informa que houve uma falha na atualização
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar regime de comunhão: {e}"
            )