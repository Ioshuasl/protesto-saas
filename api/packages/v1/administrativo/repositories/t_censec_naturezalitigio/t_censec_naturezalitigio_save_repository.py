from fastapi import HTTPException, status
from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_censec_naturezalitigio_schema import TCensecNaturezalitigioSaveSchema


class SaveRepository(BaseRepository):
    """
    Repositório para a operação de salvamento de um novo registro na tabela t_censec_naturezalitigio.
    """

    def execute(self, censec_naturezalitigio_schema: TCensecNaturezalitigioSaveSchema):
        """
        Executa a operação de salvamento no banco de dados.

        Args:
            censec_naturezalitigio_schema (TCensecNaturezalitigioSaveSchema): O esquema com os dados a serem salvos.

        Returns:
            O registro recém-criado.

        Raises:
            HTTPException: Caso ocorra um erro na execução da query.
        """
        try:

            # Montagem do SQL
            sql = """ INSERT INTO T_CENSEC_NATUREZALITIGIO(
                        CENSEC_NATUREZALITIGIO_ID,
                        DESCRICAO,
                        SITUACAO
                        ) VALUES (
                        :censec_naturezalitigio_id,
                        :descricao,
                        :situacao
                        ) RETURNING *;"""
            
            # Preenchimento de parâmetros
            params = {
                'censec_naturezalitigio_id': censec_naturezalitigio_schema.censec_naturezalitigio_id,
                'descricao': censec_naturezalitigio_schema.descricao,
                'situacao': censec_naturezalitigio_schema.situacao
            }

            # Execução do sql
            return self.run_and_return(sql, params)
        
        except Exception as e:
        
            # Informa que houve uma falha no salvamento do registro
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao salvar CENSEC_NATUREZALITIGIO: {e}"
            )