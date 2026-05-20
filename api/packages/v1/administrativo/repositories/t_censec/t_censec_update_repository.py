from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_censec_schema import TCensecUpdateSchema
from fastapi import HTTPException, status

class UpdateRepository(BaseRepository):
    """
    Repositório para a operação de atualização na tabela T_CENSEC.
    """

    def execute(self, censec_id : int, censec_schema: TCensecUpdateSchema):
        """
        Executa a atualização de um registro na tabela.
        
        Args:
            censec_id (int): O ID do registro a ser atualizado.
            censec_schema (TCensecUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O registro atualizado.
            
        Raises:
            HTTPException: Se o registro não for encontrado ou ocorrer um erro na atualização.
        """
        try:
            updates = []
            params = {}

            if censec_schema.descricao is not None:
                updates.append("DESCRICAO = :descricao")
                params["descricao"] = censec_schema.descricao

            if censec_schema.situacao is not None:
                updates.append("SITUACAO = :situacao")
                params["situacao"] = censec_schema.situacao

            if not updates:
                return False

            params["censec_id"] = censec_id
            sql = f"UPDATE T_CENSEC SET {', '.join(updates)} WHERE censec_id = :censec_id RETURNING *;"

            # Executa a query
            result = self.run_and_return(sql, params)

            if not result.censec_id:
                # Informa que não existe o registro a ser modificado
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail='Nenhum CENSEC localizado para esta solicitação'
                )
            
            # Se houver um resultado, a atualização foi bem-sucedida
            if result:
                return result

        except Exception as e:
            # Informa que houve uma falha na atualização
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar o CENSEC: {e}"
            )