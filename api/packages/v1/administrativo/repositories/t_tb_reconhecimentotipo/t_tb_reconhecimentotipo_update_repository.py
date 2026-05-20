from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_tb_reconhecimentotipo_schema import TTbReconhecimentotipoUpdateSchema
from fastapi import HTTPException, status

class UpdateRepository(BaseRepository):
    """
    Repositório para a operação de atualização na tabela T_TB_RECONHECIMENTOTIPO.
    """

    def execute(self, tb_reconhecimentotipo_id : int, reconhecimentotipo_schema: TTbReconhecimentotipoUpdateSchema):
        """
        Executa a atualização de um registro na tabela.
        
        Args:
            reconhecimentotipo_schema (T_TbReconhecimentotipoUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O registro atualizado.
            
        Raises:
            HTTPException: Se o registro não for encontrado ou ocorrer um erro na atualização.
        """
        try:
            updates = []
            params = {}

            if reconhecimentotipo_schema.descricao is not None:
                updates.append("DESCRICAO = :descricao")
                params["descricao"] = reconhecimentotipo_schema.descricao

            if reconhecimentotipo_schema.situacao is not None:
                updates.append("SITUACAO = :situacao")
                params["situacao"] = reconhecimentotipo_schema.situacao

            if not updates:
                return False

            params["tb_reconhecimentotipo_id"] = tb_reconhecimentotipo_id
            sql = f"UPDATE T_TB_RECONHECIMENTOTIPO SET {', '.join(updates)} WHERE tb_reconhecimentotipo_id = :tb_reconhecimentotipo_id RETURNING *;"

            # Executa a query
            result = self.run_and_return(sql, params)

            if not result.tb_reconhecimentotipo_id:
                # Informa que não existe o registro a ser modificado
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail='Nenhum tipo de reconhecimento localizado para esta solicitação'
                )
            
            # Se houver um resultado, a atualização foi bem-sucedida
            if result:
                return result

        except Exception as e:
            # Informa que houve uma falha na atualização
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar o tipo de reconhecimento: {e}"
            )
