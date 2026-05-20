from fastapi import HTTPException, status
from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_medida_tipo_schema import GMedidaTipoSaveSchema


class SaveRepository(BaseRepository):
    """
    Repositório para a operação de salvamento de um novo registro na tabela g_medida_tipo.
    """

    def execute(self, medida_tipo_schema: GMedidaTipoSaveSchema):
        """
        Executa a operação de salvamento no banco de dados.

        Args:
            medida_tipo_schema (GMedidaTipoSaveSchema): O esquema com os dados a serem salvos.

        Returns:
            O registro recém-criado.

        Raises:
            HTTPException: Caso ocorra um erro na execução da query.
        """
        try:

            # Montagem do SQL
            sql = """ INSERT INTO G_MEDIDA_TIPO(
                        MEDIDA_TIPO_ID,
                        DESCRICAO,
                        SIGLA
                        ) VALUES (
                        :medida_tipo_id,
                        :descricao,
                        :sigla
                        ) RETURNING *;"""
            
            # Preenchimento de parâmetros
            params = {
                'medida_tipo_id': medida_tipo_schema.medida_tipo_id,
                'descricao': medida_tipo_schema.descricao,
                'sigla': medida_tipo_schema.sigla
            }

            # Execução do sql
            return self.run_and_return(sql, params)
        
        except Exception as e:
        
            # Informa que houve uma falha no salvamento do registro
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao salvar G_MEDIDA_TIPO: {e}"
            )