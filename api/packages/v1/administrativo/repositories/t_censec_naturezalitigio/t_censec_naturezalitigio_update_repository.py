from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_censec_naturezalitigio_schema import TCensecNaturezalitigioUpdateSchema
from fastapi import HTTPException, status

class UpdateRepository(BaseRepository):
    """
    Repositório para a operação de atualização na tabela T_CENSEC_NATUREZALITIGIO.
    """

    def execute(self, censec_naturezalitigio_id : int, censec_naturezalitigio_schema: TCensecNaturezalitigioUpdateSchema):
        """
        Executa a atualização de um registro na tabela.
        
        Args:
            censec_naturezalitigio_id (int): O ID do registro a ser atualizado.
            censec_naturezalitigio_schema (TCensecNaturezalitigioUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O registro atualizado.
            
        Raises:
            HTTPException: Se o registro não for encontrado ou ocorrer um erro na atualização.
        """
        try:
            updates = []
            params = {}

            if censec_naturezalitigio_schema.descricao is not None:
                updates.append("DESCRICAO = :descricao")
                params["descricao"] = censec_naturezalitigio_schema.descricao

            if censec_naturezalitigio_schema.situacao is not None:
                updates.append("SITUACAO = :situacao")
                params["situacao"] = censec_naturezalitigio_schema.situacao

            if not updates:
                return False

            params["censec_naturezalitigio_id"] = censec_naturezalitigio_id
            sql = f"UPDATE T_CENSEC_NATUREZALITIGIO SET {', '.join(updates)} WHERE censec_naturezalitigio_id = :censec_naturezalitigio_id RETURNING *;"

            # Executa a query
            result = self.run_and_return(sql, params)

            if not result.censec_naturezalitigio_id:
                # Informa que não existe o registro a ser modificado
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail='Nenhum CENSEC_NATUREZALITIGIO localizado para esta solicitação'
                )
            
            # Se houver um resultado, a atualização foi bem-sucedida
            if result:
                return result

        except Exception as e:
            # Informa que houve uma falha na atualização
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar o CENSEC_NATUREZALITIGIO: {e}"
            )