from fastapi import HTTPException, status
from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_pessoa_representante_schema import (
    TPessoaRepresentanteSaveSchema,
)


class TPessoaRepresentanteSaveRepository(BaseRepository):
    """
    Repositório para a operação de salvamento de um novo registro na tabela g_tb_regimebens.
    """

    def execute(
        self, t_pessoa_representante_save_schema: TPessoaRepresentanteSaveSchema
    ):
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
            sql = """
            INSERT INTO T_PESSOA_REPRESENTANTE(
                REPRESENTANTE_ID,
                PESSOA_REPRESENTANTE_ID,
                PESSOA_ID,
                PESSOA_AUXILIAR_ID,
                MARCACAO_TIPO_ID,
                ATO_PARTETIPO_ID,
                ASSINATURA_TIPO
            ) VALUES (
                :representante_id,
                :pessoa_representante_id,
                :pessoa_id,
                :pessoa_auxiliar_id,
                :marcacao_tipo_id,
                :ato_partetipo_id,
                :assinatura_tipo
            ) RETURNING *;
            """

            # Preenchimento de parâmetros
            params = {
                "representante_id": t_pessoa_representante_save_schema.representante_id,
                "pessoa_representante_id": t_pessoa_representante_save_schema.pessoa_representante_id,
                "pessoa_id": t_pessoa_representante_save_schema.pessoa_id,
                "pessoa_auxiliar_id": t_pessoa_representante_save_schema.pessoa_auxiliar_id,
                "marcacao_tipo_id": t_pessoa_representante_save_schema.marcacao_tipo_id,
                "ato_partetipo_id": t_pessoa_representante_save_schema.ato_partetipo_id,
                "assinatura_tipo": t_pessoa_representante_save_schema.assinatura_tipo,
            }

            # Execução do sql
            return self.run_and_return(sql, params)

        except Exception as e:

            # Informa que houve uma falha no salvamento do registro
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao salvar registro: {e}",
            )
