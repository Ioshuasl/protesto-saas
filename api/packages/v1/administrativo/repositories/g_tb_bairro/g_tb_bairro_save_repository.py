from fastapi import HTTPException, status
from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_tb_bairro_schema import GTbBairroSaveSchema


class SaveRepository(BaseRepository):
    """
    Repositório para a operação de salvamento de um novo registro na tabela g_tb_bairro.
    """

    def execute(self, bairro_schema: GTbBairroSaveSchema):
        """
        Executa a operação de salvamento no banco de dados.

        Args:
            bairro_schema (GTbBairroSaveSchema): O esquema com os dados a serem salvos.

        Returns:
            O registro recém-criado.

        Raises:
            HTTPException: Caso ocorra um erro na execução da query.
        """
        try:

            # Montagem do SQL
            sql = """ INSERT INTO G_TB_BAIRRO(
                        TB_BAIRRO_ID,
                        DESCRICAO,
                        SITUACAO,
                        SISTEMA_ID
                        ) VALUES (
                        :tb_bairro_id,
                        :descricao,
                        :situacao,
                        :sistema_id
                        ) RETURNING *;"""
            
            # Preenchimento de parâmetros
            params = {
                'tb_bairro_id': bairro_schema.tb_bairro_id,
                'descricao': bairro_schema.descricao,
                'situacao': bairro_schema.situacao,
                'sistema_id': bairro_schema.sistema_id
            }

            # Execução do sql
            return self.run_and_return(sql, params)
        
        except Exception as e:
        
            # Informa que houve uma falha no salvamento do registro
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao salvar o Bairro: {e}"
            )