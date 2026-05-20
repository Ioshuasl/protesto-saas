from fastapi import HTTPException, status
from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_censec_tiponatureza_schema import (
    TCensecTipoNaturezaSaveSchema,
)


class TCensecTipoNaturezaSaveRepository(BaseRepository):
    """
    Repositório responsável pela operação de salvamento de um novo registro
    na tabela T_CENSEC_TIPOATO.
    """

    def execute(self, t_censec_tiponatureza_save_schema: TCensecTipoNaturezaSaveSchema):
        """
        Executa a operação de salvamento no banco de dados.

        Args:
            t_censec_tiponatureza_save_schema (TCensecTipoNaturezaSchema): O esquema com os dados a serem salvos.

        Returns:
            O registro recém-criado.

        Raises:
            HTTPException: Caso ocorra um erro na execução da query.
        """
        try:
            # ----------------------------------------------------
            # Montagem do SQL
            # ----------------------------------------------------
            sql = """
                INSERT INTO T_CENSEC_TIPONATUREZA (
                    CENSEC_TIPONATUREZA_ID,
                    CENSEC_TIPOATO_ID,
                    DESCRICAO,
                    POSSUI_ATO_ANTERIOR,
                    CODIGO,
                    OBRIGATORIO,
                    TIPO_ATO_ANTERIOR,
                    SITUACAO_ATO_ANTERIOR
                ) VALUES (
                    :censec_tiponatureza_id,
                    :censec_tipoato_id,
                    :descricao,
                    :possui_ato_anterior,
                    :codigo,
                    :obrigatorio,
                    :tipo_ato_anterior,
                    :situacao_ato_anterior
                )
                RETURNING *;
            """

            # ----------------------------------------------------
            # Preenchimento dos parâmetros
            # ----------------------------------------------------
            params = t_censec_tiponatureza_save_schema.model_dump(exclude_unset=True)

            # ----------------------------------------------------
            # Execução do SQL e retorno do registro
            # ----------------------------------------------------
            return self.run_and_return(sql, params)

        except Exception as e:
            # ----------------------------------------------------
            # Tratamento de erros e lançamento de exceção HTTP
            # ----------------------------------------------------
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao salvar registro em T_CENSEC_TIPOATO: {e}",
            )
