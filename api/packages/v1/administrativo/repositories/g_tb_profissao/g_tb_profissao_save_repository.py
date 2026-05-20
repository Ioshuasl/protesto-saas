from fastapi import HTTPException, status
from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_tb_profissao_schema import GTbProfissaoSaveSchema


class SaveRepository(BaseRepository):
    """
    Repositório para a operação de salvamento de um novo registro na tabela G_TB_PROFISSAO.
    """

    def execute(self, profissao_schema: GTbProfissaoSaveSchema):
        """
        Executa a operação de salvamento no banco de dados.

        Args:
            profissao_schema (GTbProfissaoSaveSchema): O esquema com os dados a serem salvos.

        Returns:
            O registro recém-criado.

        Raises:
            HTTPException: Caso ocorra um erro na execução da query.
        """
        try:

            # Montagem do SQL
            sql = """ INSERT INTO G_TB_PROFISSAO(
                        TB_PROFISSAO_ID,
                        DESCRICAO,
                        SITUACAO,
                        COD_CBO
                        ) VALUES (
                        :tb_profissao_id,
                        :descricao,
                        :situacao,
                        :cod_cbo
                        ) RETURNING *;"""
            
            # Preenchimento de parâmetros
            params = {
                'tb_profissao_id': profissao_schema.tb_profissao_id,
                'descricao': profissao_schema.descricao,
                'situacao': profissao_schema.situacao,
                'cod_cbo': profissao_schema.cod_cbo
            }

            # Execução do sql
            return self.run_and_return(sql, params)
        
        except Exception as e:
        
            # Informa que houve uma falha no salvamento do registro
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao salvar profissão: {e}"
            )