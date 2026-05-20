from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_censec_naturezalitigio_schema import TCensecNaturezalitigioIdSchema
from fastapi import HTTPException, status

class ShowRepository(BaseRepository):
    """
    Repositório para a operação de exibição de um registro na tabela t_censec_naturezalitigio.
    """

    def execute(self, censec_naturezalitigio_schema: TCensecNaturezalitigioIdSchema):
        """
        Busca um registro específico de CENSEC_NATUREZALITIGIO pelo ID.

        Args:
            censec_naturezalitigio_schema (TCensecNaturezalitigioIdSchema): O esquema que contém o ID do registro.

        Returns:
            O registro encontrado ou None se não existir.

        Raises:
            HTTPException: Caso ocorra um erro na execução da query.
        """
        try:
            # Montagem do SQL
            sql = "SELECT * FROM T_CENSEC_NATUREZALITIGIO WHERE CENSEC_NATUREZALITIGIO_ID = :censec_naturezalitigio_id"

            # Preenchimento de parâmetros
            params = {
                'censec_naturezalitigio_id': censec_naturezalitigio_schema.censec_naturezalitigio_id
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