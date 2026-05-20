from fastapi import HTTPException, status
from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_tb_regimebens_schema import GTbRegimebensSaveSchema


class SaveRepository(BaseRepository):
    """
    Repositório para a operação de salvamento de um novo registro na tabela g_tb_regimebens.
    """

    def execute(self, regimebens_schema: GTbRegimebensSaveSchema):
        """
        Executa a operação de salvamento no banco de dados.

        Args:
            regimebens_schema (GTbRegimebensSaveSchema): O esquema com os dados a serem salvos.

        Returns:
            O registro recém-criado.

        Raises:
            HTTPException: Caso ocorra um erro na execução da query.
        """
        try:

            # Montagem do SQL
            sql = """ INSERT INTO G_TB_REGIMEBENS(
                        TB_REGIMEBENS_ID,
                        DESCRICAO,
                        SITUACAO
                        ) VALUES (
                        :tb_regimebens_id,
                        :descricao,
                        :situacao
                        ) RETURNING *;"""

            # Preenchimento de parâmetros
            params = {
                'tb_regimebens_id': regimebens_schema.tb_regimebens_id,
                'descricao': regimebens_schema.descricao,
                'situacao': regimebens_schema.situacao
            }

            # Execução do sql
            return self.run_and_return(sql, params)

        except Exception as e:

            # Informa que houve uma falha no salvamento do registro
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao salvar registro: {e}"
            )