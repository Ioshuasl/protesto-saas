from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_tb_reconhecimentotipo_schema import TTbReconhecimentotipoIdSchema
from fastapi import HTTPException, status

class ShowRepository(BaseRepository):
    """
    Repositório para a operação de exibição de um registro na tabela t_tb_reconhecimentotipo.
    """

    def execute(self, reconhecimentotipo_schema: TTbReconhecimentotipoIdSchema):
        """
        Busca um tipo de reconhecimento específico pelo ID.

        Args:
            reconhecimentotipo_schema (T_TbReconhecimentotipoIdSchema): O esquema que contém o ID do registro.

        Returns:
            O registro encontrado ou None se não existir.

        Raises:
            HTTPException: Caso ocorra um erro na execução da query.
        """
        try:
            # Montagem do SQL
            sql = "SELECT * FROM T_TB_RECONHECIMENTOTIPO WHERE TB_RECONHECIMENTOTIPO_ID = :tb_reconhecimentotipo_id"

            # Preenchimento de parâmetros
            params = {
                'tb_reconhecimentotipo_id': reconhecimentotipo_schema.tb_reconhecimentotipo_id
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
