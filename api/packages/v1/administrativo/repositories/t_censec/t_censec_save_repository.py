from fastapi import HTTPException, status
from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_censec_schema import TCensecSaveSchema


class SaveRepository(BaseRepository):
    """
    Repositório para a operação de salvamento de um novo registro na tabela t_censec.
    """

    def execute(self, censec_schema: TCensecSaveSchema):
        """
        Executa a operação de salvamento no banco de dados.

        Args:
            censec_schema (TCensecSaveSchema): O esquema com os dados a serem salvos.

        Returns:
            O registro recém-criado.

        Raises:
            HTTPException: Caso ocorra um erro na execução da query.
        """
        try:

            # Montagem do SQL
            sql = """ INSERT INTO T_CENSEC(
                        CENSEC_ID,
                        DESCRICAO,
                        SITUACAO
                        ) VALUES (
                        :censec_id,
                        :descricao,
                        :situacao
                        ) RETURNING *;"""
            
            # Preenchimento de parâmetros
            params = {
                'censec_id': censec_schema.censec_id,
                'descricao': censec_schema.descricao,
                'situacao': censec_schema.situacao
            }

            # Execução do sql
            return self.run_and_return(sql, params)
        
        except Exception as e:
        
            # Informa que houve uma falha no salvamento do registro
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao salvar CENSEC: {e}"
            )