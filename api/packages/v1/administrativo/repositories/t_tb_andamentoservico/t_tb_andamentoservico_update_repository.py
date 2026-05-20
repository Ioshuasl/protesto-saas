from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_tb_andamentoservico_schema import TTbAndamentoservicoUpdateSchema
from fastapi import HTTPException, status

class UpdateRepository(BaseRepository):
    """
    Repositório para a operação de atualização na tabela T_TB_ANDAMENTOSERVICO.
    """

    def execute(self, tb_andamentoservico_id: int, andamentoservico_schema: TTbAndamentoservicoUpdateSchema):
        """
        Executa a atualização de um registro na tabela.
        
        Args:
            andamentoservico_schema (TTbAndamentoservicoUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O registro atualizado.
            
        Raises:
            HTTPException: Se o registro não for encontrado ou ocorrer um erro na atualização.
        """
        try:
            updates = []
            params = {}

            if andamentoservico_schema.descricao is not None:
                updates.append("DESCRICAO = :descricao")
                params["descricao"] = andamentoservico_schema.descricao

            if andamentoservico_schema.situacao is not None:
                updates.append("SITUACAO = :situacao")
                params["situacao"] = andamentoservico_schema.situacao

            if andamentoservico_schema.tipo is not None:
                updates.append("TIPO = :tipo")
                params["tipo"] = andamentoservico_schema.tipo

            if andamentoservico_schema.usa_email is not None:
                updates.append("USA_EMAIL = :usa_email")
                params["usa_email"] = andamentoservico_schema.usa_email

            if not updates:
                return False

            params["tb_andamentoservico_id"] = tb_andamentoservico_id
            sql = f"UPDATE T_TB_ANDAMENTOSERVICO SET {', '.join(updates)} WHERE tb_andamentoservico_id = :tb_andamentoservico_id RETURNING *;"

            # Executa a query
            result = self.run_and_return(sql, params)

            if not result:
                # Informa que não existe o registro a ser modificado
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail='Nenhum andamento de serviço localizado para esta solicitação'
                )
            
            # Se houver um resultado, a atualização foi bem-sucedida
            return result

        except Exception as e:
            # Informa que houve uma falha na atualização
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar o andamento de serviço: {e}"
            )