from fastapi import HTTPException, status
from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_tb_estadocivil_schema import GTbEstadoCivilSaveSchema


class SaveRepository(BaseRepository):
    """
    Repositório para a operação de salvamento de um novo registro na tabela G_TB_ESTADOCIVIL.
    """

    def execute(self, estado_civil_schema: GTbEstadoCivilSaveSchema):
        """
        Executa a operação de salvamento no banco de dados.

        Args:
            estado_civil_schema (GTBEstadoCivilSaveSchema): O esquema com os dados a serem salvos.

        Returns:
            O registro recém-criado.

        Raises:
            HTTPException: Caso ocorra um erro na execução da query.
        """
        try:

            # Montagem do SQL
            sql = """ INSERT INTO G_TB_ESTADOCIVIL(
                        TB_ESTADOCIVIL_ID,
                        DESCRICAO,
                        SITUACAO,
                        SISTEMA_ID,
                        TIPO
                        ) VALUES (
                        :tb_estadocivil_id,
                        :descricao,
                        :situacao,
                        :sistema_id,
                        :tipo
                        ) RETURNING *;"""
            
            # Preenchimento de parâmetros
            params = {
                'tb_estadocivil_id': estado_civil_schema.tb_estadocivil_id,
                'descricao': estado_civil_schema.descricao,
                'situacao': estado_civil_schema.situacao,
                'sistema_id': estado_civil_schema.sistema_id,
                'tipo': estado_civil_schema.tipo
            }

            # Execução do sql
            return self.run_and_return(sql, params)
        
        except Exception as e:
        
            # Informa que houve uma falha no salvamento do registro
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao salvar Estado Civil: {e}"
            )