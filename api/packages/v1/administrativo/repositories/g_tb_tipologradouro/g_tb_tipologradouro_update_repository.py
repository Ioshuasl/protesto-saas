from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_tb_tipologradouro_schema import GTbTipoLogradouroUpdateSchema
from fastapi import HTTPException, status

class UpdateRepository(BaseRepository):
    """
    Repositório para a operação de atualização na tabela G_TB_TIPOLOGRADOURO.
    """

    def execute(self, tipologradouro_id : int, tipologradouro_schema: GTbTipoLogradouroUpdateSchema):
        """
        Executa a atualização de um registro na tabela.
        
        Args:
            tipologradouro_id (int): O ID do registro a ser atualizado.
            tipologradouro_schema (GTbTipoLogradouroUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O registro atualizado.
            
        Raises:
            HTTPException: Se o registro não for encontrado ou ocorrer um erro na atualização.
        """
        try:
            updates = []
            params = {}

            if tipologradouro_schema.descricao is not None:
                updates.append("DESCRICAO = :descricao")
                params["descricao"] = tipologradouro_schema.descricao

            if tipologradouro_schema.situacao is not None:
                updates.append("SITUACAO = :situacao")
                params["situacao"] = tipologradouro_schema.situacao

            if tipologradouro_schema.sistema_id is not None:
                updates.append("SISTEMA_ID = :sistema_id")
                params["sistema_id"] = tipologradouro_schema.sistema_id


            if not updates:
                return False

            params["tb_tipologradouro_id"] = tipologradouro_id
            sql = f"UPDATE G_TB_TIPOLOGRADOURO SET {', '.join(updates)} WHERE TB_TIPOLOGRADOURO_ID = :tb_tipologradouro_id RETURNING *;"

            # Executa a query
            result = self.run_and_return(sql, params)

            if not result:
                # Informa que não existe o registro a ser modificado
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail='Nenhum G_TB_TIPOLOGRADOURO localizado para esta solicitação'
                )
            
            # Se houver um resultado, a atualização foi bem-sucedida
            if result:
                return result

        except Exception as e:
            # Informa que houve uma falha na atualização
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar o G_TB_TIPOLOGRADOURO: {e}"
            )