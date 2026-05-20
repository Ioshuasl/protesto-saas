from fastapi import HTTPException, status
from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_censec_qualidade_schema import TCensecQualidadeSaveSchema


class SaveRepository(BaseRepository):
    """
    Repositório para a operação de salvamento de um novo registro na tabela t_censec_qualidade.
    """

    def execute(self, censec_qualidade_schema: TCensecQualidadeSaveSchema):
        """
        Executa a operação de salvamento no banco de dados.

        Args:
            censec_qualidade_schema (TCensecQualidadeSaveSchema): O esquema com os dados a serem salvos.

        Returns:
            O registro recém-criado.

        Raises:
            HTTPException: Caso ocorra um erro na execução da query.
        """
        try:

            # Montagem do SQL
            sql = """ INSERT INTO T_CENSEC_QUALIDADE(
                        CENSEC_QUALIDADE_ID,
                        DESCRICAO,
                        SITUACAO,
                        ACEITA_CNPJ
                        ) VALUES (
                        :censec_qualidade_id,
                        :descricao,
                        :situacao,
                        :aceita_cnpj
                        ) RETURNING *;"""
            
            # Preenchimento de parâmetros
            params = {
                'censec_qualidade_id': censec_qualidade_schema.censec_qualidade_id,
                'descricao': censec_qualidade_schema.descricao,
                'situacao': censec_qualidade_schema.situacao,
                'aceita_cnpj': censec_qualidade_schema.aceita_cnpj
            }

            # Execução do sql
            return self.run_and_return(sql, params)
        
        except Exception as e:
        
            # Informa que houve uma falha no salvamento do registro
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao salvar CENSEC_QUALIDADE: {e}"
            )