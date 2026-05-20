from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_minuta_schema import TMinutaUpdateSchema
from fastapi import HTTPException, status

class UpdateRepository(BaseRepository):
    """
    Repositório para a operação de atualização na tabela T_MINUTA.
    """

    def execute(self, minuta_id: int, minuta_schema: TMinutaUpdateSchema):
        """
        Executa a atualização de um registro na tabela.
        
        Args:
            minuta_id (int): O ID do registro a ser atualizado.
            minuta_schema (TMinutaUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O registro atualizado.
            
        Raises:
            HTTPException: Se o registro não for encontrado ou ocorrer um erro na atualização.
        """
        try:
            updates = []
            params = {}

            if minuta_schema.ato_tipo_id is not None:
                updates.append("ATO_TIPO_ID = :ato_tipo_id")
                params["ato_tipo_id"] = minuta_schema.ato_tipo_id
            
            if minuta_schema.natureza_id is not None:
                updates.append("NATUREZA_ID = :natureza_id")
                params["natureza_id"] = minuta_schema.natureza_id
            
            if minuta_schema.descricao is not None:
                updates.append("DESCRICAO = :descricao")
                params["descricao"] = minuta_schema.descricao

            if minuta_schema.texto is not None:
                updates.append("TEXTO = :texto")
                params["texto"] = minuta_schema.texto
            
            if minuta_schema.protegida is not None:
                updates.append("PROTEGIDA = :protegida")
                params["protegida"] = minuta_schema.protegida
            
            if minuta_schema.situacao is not None:
                updates.append("SITUACAO = :situacao")
                params["situacao"] = minuta_schema.situacao

            if not updates:
                return False

            params["minuta_id"] = minuta_id
            sql = f"UPDATE T_MINUTA SET {', '.join(updates)} WHERE minuta_id = :minuta_id RETURNING *;"

            # Executa a query
            result = self.run_and_return(sql, params)

            if not result.minuta_id:
                # Informa que não existe o registro a ser modificado
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail='Nenhuma MINUTA localizada para esta solicitação'
                )
            
            # Se houver um resultado, a atualização foi bem-sucedida
            if result:
                return result

        except Exception as e:
            # Informa que houve uma falha na atualização
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar a MINUTA: {e}"
            )