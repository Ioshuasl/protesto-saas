from abstracts.repository import BaseRepository
from fastapi import HTTPException, status

from packages.v1.administrativo.repositories.t_pessoa_representante.t_pessoa_representante_delete_repository import (
    TPessoaRepresentanteIdSchema,
)


class TPessoaRepresentanteShowRepository(BaseRepository):
    """
    Repositório para a operação de exibição de um registro na tabela g_tb_regimebens.
    """

    def execute(self, t_pessoa_representante_id_schema: TPessoaRepresentanteIdSchema):
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
            sql = "SELECT * FROM T_PESSOA_REPRESENTANTE TPR WHERE TPR.PESSOA_REPRESENTANTE_ID = :pessoa_representante_id;"

            # Preenchimento de parâmetros
            params = {
                "pessoa_representante_id": t_pessoa_representante_id_schema.pessoa_representante_id
            }

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
