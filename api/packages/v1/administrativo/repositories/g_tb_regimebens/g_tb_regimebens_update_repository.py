from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_tb_regimebens_schema import GTbRegimebensUpdateSchema
from fastapi import HTTPException, status

class UpdateRepository(BaseRepository):
    """
    Repositório para a operação de atualização na tabela G_TB_REGIMEBENS.
    """

    def execute(self, tb_regimebens_id: int, regimebens_schema: GTbRegimebensUpdateSchema):
        """
        Executa a atualização de um registro na tabela.

        Args:
            regimebens_schema (GTbRegimebensUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O registro atualizado.

        Raises:
            HTTPException: Se o registro não for encontrado ou ocorrer um erro na atualização.
        """
        try:
            updates = []
            params = {}

            if regimebens_schema.descricao is not None:
                updates.append("DESCRICAO = :descricao")
                params["descricao"] = regimebens_schema.descricao

            if regimebens_schema.situacao is not None:
                updates.append("SITUACAO = :situacao")
                params["situacao"] = regimebens_schema.situacao

            if not updates:
                return False

            params["tb_regimebens_id"] = tb_regimebens_id
            sql = f"UPDATE G_TB_REGIMEBENS SET {', '.join(updates)} WHERE tb_regimebens_id = :tb_regimebens_id RETURNING *;"

            # Executa a query
            result = self.run_and_return(sql, params)

            if not result.tb_regimebens_id:
                # Informa que não existe o registro a ser modificado
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail='Nenhum regime de bens localizado para esta solicitação'
                )

            # Se houver um resultado, a atualização foi bem-sucedida
            if result:
                return result

        except Exception as e:
            # Informa que houve uma falha na atualização
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar o regime de bens: {e}"
            )