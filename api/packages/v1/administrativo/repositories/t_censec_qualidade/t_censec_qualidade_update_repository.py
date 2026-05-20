from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_censec_qualidade_schema import TCensecQualidadeUpdateSchema
from fastapi import HTTPException, status

class UpdateRepository(BaseRepository):
    """
    Repositório para a operação de atualização na tabela T_CENSEC_QUALIDADE.
    """

    def execute(self, censec_qualidade_id : int, censec_qualidade_schema: TCensecQualidadeUpdateSchema):
        """
        Executa a atualização de um registro na tabela.
        
        Args:
            censec_qualidade_id (int): O ID do registro a ser atualizado.
            censec_qualidade_schema (TCensecQualidadeUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O registro atualizado.
            
        Raises:
            HTTPException: Se o registro não for encontrado ou ocorrer um erro na atualização.
        """
        try:
            updates = []
            params = {}

            if censec_qualidade_schema.descricao is not None:
                updates.append("DESCRICAO = :descricao")
                params["descricao"] = censec_qualidade_schema.descricao

            if censec_qualidade_schema.situacao is not None:
                updates.append("SITUACAO = :situacao")
                params["situacao"] = censec_qualidade_schema.situacao
                
            if censec_qualidade_schema.aceita_cnpj is not None:
                updates.append("ACEITA_CNPJ = :aceita_cnpj")
                params["aceita_cnpj"] = censec_qualidade_schema.aceita_cnpj

            if not updates:
                return False

            params["censec_qualidade_id"] = censec_qualidade_id
            sql = f"UPDATE T_CENSEC_QUALIDADE SET {', '.join(updates)} WHERE censec_qualidade_id = :censec_qualidade_id RETURNING *;"

            # Executa a query
            result = self.run_and_return(sql, params)

            if not result.censec_qualidade_id:
                # Informa que não existe o registro a ser modificado
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail='Nenhum CENSEC_QUALIDADE localizado para esta solicitação'
                )
            
            # Se houver um resultado, a atualização foi bem-sucedida
            if result:
                return result

        except Exception as e:
            # Informa que houve uma falha na atualização
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar o CENSEC_QUALIDADE: {e}"
            )