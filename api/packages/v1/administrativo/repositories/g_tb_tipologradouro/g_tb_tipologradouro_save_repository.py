from fastapi import HTTPException, status
from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_tb_tipologradouro_schema import GTbTipoLogradouroSaveSchema


class SaveRepository(BaseRepository):
    """
    Repositório para a operação de salvamento de um novo registro na tabela g_tb_tipologradouro.
    """

    def execute(self, tipologradouro_schema: GTbTipoLogradouroSaveSchema):
        """
        Executa a operação de salvamento no banco de dados.

        Args:
            tipologradouro_schema (GTbTipoLogradouroSaveSchema): O esquema com os dados a serem salvos.

        Returns:
            O registro recém-criado.

        Raises:
            HTTPException: Caso ocorra um erro na execução da query.
        """
        try:
            # Montagem do SQL
            sql = """ INSERT INTO G_TB_TIPOLOGRADOURO(
                        TB_TIPOLOGRADOURO_ID,
                        DESCRICAO,
                        SITUACAO,
                        SISTEMA_ID,
                        SITUACAO_ID,
                        ONR_TIPO_LOGRADOURO_ID
                        ) VALUES (
                        :tb_tipologradouro_id,
                        :descricao,
                        :situacao,
                        :sistema_id,
                        :situacao_id,
                        :onr_tipo_logradouro_id
                        ) RETURNING *;"""
            
            # Preenchimento de parâmetros
            params = {
                'tb_tipologradouro_id': tipologradouro_schema.tb_tipologradouro_id,
                'descricao': tipologradouro_schema.descricao,
                'situacao': tipologradouro_schema.situacao,
                'sistema_id': tipologradouro_schema.sistema_id,
                'situacao_id': tipologradouro_schema.situacao_id,
                'onr_tipo_logradouro_id': tipologradouro_schema.onr_tipo_logradouro_id
            }

            # Execução do sql
            return self.run_and_return(sql, params)
        
        except Exception as e:
        
            # Informa que houve uma falha no salvamento do registro
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao salvar G_TB_TIPOLOGRADOURO: {e}"
            )