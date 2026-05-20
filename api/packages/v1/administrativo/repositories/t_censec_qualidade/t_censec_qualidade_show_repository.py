from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_censec_qualidade_schema import TCensecQualidadeIdSchema
from fastapi import HTTPException, status

class ShowRepository(BaseRepository):
    """
    Repositório para a operação de exibição de um registro na tabela t_censec_qualidade.
    """

    def execute(self, censec_qualidade_schema: TCensecQualidadeIdSchema):
        """
        Busca um registro específico de CENSEC_QUALIDADE pelo ID.

        Args:
            censec_qualidade_schema (TCensecQualidadeIdSchema): O esquema que contém o ID do registro.

        Returns:
            O registro encontrado ou None se não existir.

        Raises:
            HTTPException: Caso ocorra um erro na execução da query.
        """
        try:
            # Montagem do SQL
            sql = "SELECT * FROM T_CENSEC_QUALIDADE WHERE CENSEC_QUALIDADE_ID = :censec_qualidade_id"

            # Preenchimento de parâmetros
            params = {
                'censec_qualidade_id': censec_qualidade_schema.censec_qualidade_id
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