from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_censec_schema import TCensecIdSchema
from fastapi import HTTPException, status

class ShowRepository(BaseRepository):
    """
    Repositório para a operação de exibição de um registro na tabela t_censec.
    """

    def execute(self, censec_schema: TCensecIdSchema):
        """
        Busca um registro específico de CENSEC pelo ID.

        Args:
            censec_schema (TCensecIdSchema): O esquema que contém o ID do registro.

        Returns:
            O registro encontrado ou None se não existir.

        Raises:
            HTTPException: Caso ocorra um erro na execução da query.
        """
        try:
            # Montagem do SQL
            sql = "SELECT * FROM T_CENSEC WHERE CENSEC_ID = :censec_id"

            # Preenchimento de parâmetros
            params = {
                'censec_id': censec_schema.censec_id
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