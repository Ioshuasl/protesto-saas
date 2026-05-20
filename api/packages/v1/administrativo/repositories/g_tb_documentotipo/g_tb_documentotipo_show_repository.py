from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_tb_documentotipo_schema import GTbDocumentoTipoIdSchema
from fastapi import HTTPException, status

class ShowRepository(BaseRepository):
    """
    Repositório para a operação de exibição de um registro na tabela G_TB_DOCUMENTOTIPO.
    """

    def execute(self, documentotipo_schema: GTbDocumentoTipoIdSchema):
        """
        Busca um registro específico de G_TB_DOCUMENTOTIPO pelo ID.

        Args:
            documentotipo_schema (GtbDocumentotipoIdSchema): O esquema que contém o ID do registro.

        Returns:
            O registro encontrado ou None se não existir.

        Raises:
            HTTPException: Caso ocorra um erro na execução da query.
        """
        try:
            # Montagem do SQL
            sql = "SELECT * FROM G_TB_DOCUMENTOTIPO WHERE TB_DOCUMENTOTIPO_ID = :tb_documentotipo_id"

            # Preenchimento de parâmetros
            params = {
                'tb_documentotipo_id': documentotipo_schema.tb_documentotipo_id
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