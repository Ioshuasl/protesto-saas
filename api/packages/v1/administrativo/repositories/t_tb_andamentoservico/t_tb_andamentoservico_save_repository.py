from fastapi import HTTPException, status
from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_tb_andamentoservico_schema import TTbAndamentoservicoSaveSchema


class SaveRepository(BaseRepository):
    """
    Repositório para a operação de salvamento de um novo registro na tabela t_tb_andamentoservico.
    """

    def execute(self, andamentoservico_schema: TTbAndamentoservicoSaveSchema):
        """
        Executa a operação de salvamento no banco de dados.

        Args:
            andamentoservico_schema (TTbAndamentoservicoSaveSchema): O esquema com os dados a serem salvos.

        Returns:
            O registro recém-criado.

        Raises:
            HTTPException: Caso ocorra um erro na execução da query.
        """
        try:

            # Montagem do SQL
            sql = """ INSERT INTO T_TB_ANDAMENTOSERVICO(
                        TB_ANDAMENTOSERVICO_ID,
                        DESCRICAO,
                        SITUACAO,
                        TIPO,
                        USA_EMAIL
                        ) VALUES (
                        :tb_andamentoservico_id,
                        :descricao,
                        :situacao,
                        :tipo,
                        :usa_email
                        ) RETURNING *;"""
            
            # Preenchimento de parâmetros
            params = {
                'tb_andamentoservico_id': andamentoservico_schema.tb_andamentoservico_id,
                'descricao': andamentoservico_schema.descricao,
                'situacao': andamentoservico_schema.situacao,
                'tipo': andamentoservico_schema.tipo,
                'usa_email': andamentoservico_schema.usa_email
            }

            # Execução do sql
            return self.run_and_return(sql, params)
        
        except Exception as e:
        
            # Informa que houve uma falha no salvamento do registro
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao salvar andamento de serviço: {e}"
            )        