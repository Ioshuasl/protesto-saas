from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_medida_tipo_schema import GMedidaTipoIdSchema
from fastapi import HTTPException, status

class ShowRepository(BaseRepository):
    """
    Repositório para a operação de exibição de um registro na tabela g_medida_tipo.
    """

    def execute(self, medida_tipo_schema: GMedidaTipoIdSchema):
        """
        Busca um registro específico de G_MEDIDA_TIPO pelo ID.

        Args:
            medida_tipo_schema (GMedidaTipoIdSchema): O esquema que contém o ID do registro.

        Returns:
            O registro encontrado ou None se não existir.

        Raises:
            HTTPException: Caso ocorra um erro na execução da query.
        """
        try:
            # Montagem do SQL
            sql = "SELECT * FROM G_MEDIDA_TIPO WHERE MEDIDA_TIPO_ID = :medida_tipo_id"

            # Preenchimento de parâmetros
            params = {
                'medida_tipo_id': medida_tipo_schema.medida_tipo_id
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