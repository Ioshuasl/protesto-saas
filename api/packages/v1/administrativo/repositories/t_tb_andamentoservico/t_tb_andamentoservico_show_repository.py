from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_tb_andamentoservico_schema import TTbAndamentoservicoIdSchema
from fastapi import HTTPException, status

class ShowRepository(BaseRepository):
    """
    Repositório para a operação de exibição de um registro na tabela t_tb_andamentoservico.
    """

    def execute(self, andamentoservico_schema: TTbAndamentoservicoIdSchema):
        """
        Busca um andamento de serviço específico pelo ID.

        Args:
            andamentoservico_schema (TTbAndamentoservicoIdSchema): O esquema que contém o ID do registro.

        Returns:
            O registro encontrado.

        Raises:
            HTTPException: Caso ocorra um erro na execução da query ou o registro não seja encontrado.
        """
        try:
            # Montagem do SQL
            sql = "SELECT * FROM T_TB_ANDAMENTOSERVICO WHERE TB_ANDAMENTOSERVICO_ID = :tb_andamentoservico_id"

            # Preenchimento de parâmetros
            params = {
                'tb_andamentoservico_id': andamentoservico_schema.tb_andamentoservico_id
            }

            # Execução do SQL
            result = self.fetch_one(sql, params)

            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Registro não encontrado"
                )

            return result
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao buscar registro: {str(e)}"
            )