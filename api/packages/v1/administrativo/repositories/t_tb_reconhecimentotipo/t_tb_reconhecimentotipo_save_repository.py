from fastapi import HTTPException, status
from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_tb_reconhecimentotipo_schema import TTbReconhecimentotipoSaveSchema


class SaveRepository(BaseRepository):
    """
    Repositório para a operação de salvamento de um novo registro na tabela t_tb_reconhecimentotipo.
    """

    def execute(self, reconhecimentotipo_schema: TTbReconhecimentotipoSaveSchema):
        """
        Executa a operação de salvamento no banco de dados.

        Args:
            reconhecimentotipo_schema (T_TbReconhecimentotipoSaveSchema): O esquema com os dados a serem salvos.

        Returns:
            O registro recém-criado.

        Raises:
            HTTPException: Caso ocorra um erro na execução da query.
        """
        try:

            # Montagem do SQL
            sql = """ INSERT INTO T_TB_RECONHECIMENTOTIPO(
                        TB_RECONHECIMENTOTIPO_ID,
                        DESCRICAO,
                        SITUACAO
                        ) VALUES (
                        :tb_reconhecimentotipo_id,
                        :descricao,
                        :situacao
                        ) RETURNING *;"""
            
            # Preenchimento de parâmetros
            params = {
                'tb_reconhecimentotipo_id': reconhecimentotipo_schema.tb_reconhecimentotipo_id,
                'descricao': reconhecimentotipo_schema.descricao,
                'situacao': reconhecimentotipo_schema.situacao
            }

            # Execução do sql
            return self.run_and_return(sql, params)
        
        except Exception as e:
        
            # Informa que houve uma falha no salvamento do registro
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao salvar registro: {e}"
            )
