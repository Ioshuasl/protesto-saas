from fastapi import HTTPException, status
from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_medida_tipo_schema import GMedidaTipoUpdateSchema


class UpdateRepository(BaseRepository):
    """
    Repositório para a operação de atualização de um registro na tabela
    g_medida_tipo.
    """

    def execute(self, medida_tipo_id: int, medida_tipo_schema: GMedidaTipoUpdateSchema):
        """
        Executa a operação de atualização no banco de dados.

        Args:
            medida_tipo_id (int): O ID do registro a ser atualizado.
            medida_tipo_schema (GMedidaTipoUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O registro atualizado.

        Raises:
            HTTPException: Caso ocorra um erro na execução da query.
        """
        try:
            # Montagem do SQL
            sql = """ UPDATE G_MEDIDA_TIPO SET
                        DESCRICAO = :descricao,
                        SIGLA = :sigla
                    WHERE MEDIDA_TIPO_ID = :medida_tipo_id
                    RETURNING *;"""
            
            # Preenchimento de parâmetros
            params = {
                'descricao': medida_tipo_schema.descricao,
                'sigla': medida_tipo_schema.sigla,
                'medida_tipo_id': medida_tipo_id
            }

            # Execução do sql
            return self.run_and_return(sql, params)
        
        except Exception as e:
        
            # Informa que houve uma falha na atualização do registro
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar G_MEDIDA_TIPO: {e}"
            )