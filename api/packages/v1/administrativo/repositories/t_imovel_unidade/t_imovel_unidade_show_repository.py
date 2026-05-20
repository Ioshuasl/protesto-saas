from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_imovel_unidade_schema import TImovelUnidadeIdSchema
from fastapi import HTTPException, status

class TImovelUnidadeShowRepository(BaseRepository):
    """
    Repositório para a operação de exibição de um registro na tabela t_censec_qualidade.
    """

    def execute(self, t_imovel_unidade_id_schema: TImovelUnidadeIdSchema):
        """
        Busca um registro específico de CENSEC_QUALIDADE pelo ID.

        Args:
            t_imovel_unidade_schema (TImovelUnidadeIdSchema): O esquema que contém o ID do registro.

        Returns:
            O registro encontrado ou None se não existir.

        Raises:
            HTTPException: Caso ocorra um erro na execução da query.
        """
        try:
            # Montagem do SQL
            sql = "SELECT * FROM T_IMOVEL_UNIDADE WHERE IMOVEL_UNIDADE_ID = :imovel_unidade_id"

            # Preenchimento de parâmetros
            params = {
                'imovel_unidade_id': t_imovel_unidade_id_schema.imovel_unidade_id
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
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao buscar registro: {str(e)}"
            )