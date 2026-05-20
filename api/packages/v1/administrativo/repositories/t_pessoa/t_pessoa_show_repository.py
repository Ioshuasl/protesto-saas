from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_pessoa_schema import TPessoaIdSchema
from fastapi import HTTPException, status


class TPessoaShowRepository(BaseRepository):
    """
    Repositório para a operação de exibição de um registro na tabela g_tb_regimebens.
    """

    def execute(self, t_pessoa_id_schema: TPessoaIdSchema):
        """
        Busca um tipo de regime de bens específico pelo ID.

        Args:
            regimebens_schema (GTbRegimebensIdSchema): O esquema que contém o ID do registro.

        Returns:
            O registro encontrado ou None se não existir.

        Raises:
            HTTPException: Caso ocorra um erro na execução da query.
        """
        try:
            # Montagem do SQL
            sql = """SELECT TP.*, TPC.pessoa_cartao_id FROM T_PESSOA TP
                     LEFT JOIN T_PESSOA_CARTAO TPC ON TP.PESSOA_ID = TPC.PESSOA_ID
                     WHERE TP.PESSOA_ID = :pessoa_id"""

            # Preenchimento de parâmetros
            params = {"pessoa_id": t_pessoa_id_schema.pessoa_id}

            # Execução do SQL
            result = self.fetch_one(sql, params)

            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Registro não encontrado",
                )

            return result
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao buscar registro: {str(e)}",
            )
