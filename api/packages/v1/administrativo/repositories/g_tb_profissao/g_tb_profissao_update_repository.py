from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_tb_profissao_schema import GTbProfissaoUpdateSchema
from fastapi import HTTPException, status

class UpdateRepository(BaseRepository):
    """
    Repositório para a operação de atualização na tabela G_TB_PROFISSAO.
    """

    def execute(self, tb_profissao_id : float, profissao_schema: GTbProfissaoUpdateSchema):
        """
        Executa a atualização de um registro na tabela.
        
        Args:
            tb_profissao_id (float): O ID da profissão a ser atualizada.
            profissao_schema (GTbProfissaoUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O registro atualizado.
            
        Raises:
            HTTPException: Se o registro não for encontrado ou ocorrer um erro na atualização.
        """
        try:
            updates = []
            params = {}

            if profissao_schema.descricao is not None:
                updates.append("DESCRICAO = :descricao")
                params["descricao"] = profissao_schema.descricao

            if profissao_schema.situacao is not None:
                updates.append("SITUACAO = :situacao")
                params["situacao"] = profissao_schema.situacao
            
            if profissao_schema.cod_cbo is not None:
                updates.append("COD_CBO = :cod_cbo")
                params["cod_cbo"] = profissao_schema.cod_cbo

            if not updates:
                return False

            params["tb_profissao_id"] = tb_profissao_id
            sql = f"UPDATE G_TB_PROFISSAO SET {', '.join(updates)} WHERE tb_profissao_id = :tb_profissao_id RETURNING *;"

            # Executa a query
            result = self.run_and_return(sql, params)

            if not result:
                # Informa que não existe o registro a ser modificado
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail='Nenhuma profissão localizada para esta solicitação'
                )
            
            # Se houver um resultado, a atualização foi bem-sucedida
            return result

        except Exception as e:
            # Informa que houve uma falha na atualização
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar profissão: {e}"
            )