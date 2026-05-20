from fastapi import HTTPException, status
from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_minuta_schema import TMinutaSaveSchema


class SaveRepository(BaseRepository):
    """
    Repositório para a operação de salvamento de um novo registro na tabela t_minuta.
    """

    def execute(self, minuta_schema: TMinutaSaveSchema):
        """
        Executa a operação de salvamento no banco de dados.

        Args:
            minuta_schema (TMinutaSaveSchema): O esquema com os dados a serem salvos.

        Returns:
            O registro recém-criado.

        Raises:
            HTTPException: Caso ocorra um erro na execução da query.
        """
        try:

            # Montagem do SQL
            sql = """ INSERT INTO T_MINUTA(
                        MINUTA_ID,
                        ATO_TIPO_ID,
                        NATUREZA_ID,
                        DESCRICAO,
                        TEXTO,
                        PROTEGIDA,
                        SITUACAO
                        ) VALUES (
                        :minuta_id,
                        :ato_tipo_id,
                        :natureza_id,
                        :descricao,
                        :texto,
                        :protegida,
                        :situacao
                        ) RETURNING *;"""

            # Preenchimento de parâmetros
            params = {
                'minuta_id': minuta_schema.minuta_id,
                'ato_tipo_id': minuta_schema.ato_tipo_id,
                'natureza_id': minuta_schema.natureza_id,
                'descricao': minuta_schema.descricao,
                'texto': minuta_schema.texto,
                'protegida': minuta_schema.protegida,
                'situacao': minuta_schema.situacao
            }

            # Execução do sql
            return self.run_and_return(sql, params)

        except Exception as e:

            # Informa que houve uma falha no salvamento do registro
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao salvar MINUTA: {e}"
            )