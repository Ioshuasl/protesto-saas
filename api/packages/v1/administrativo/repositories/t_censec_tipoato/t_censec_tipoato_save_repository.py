from fastapi import HTTPException, status
from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_censec_tipoato_schema import (
    TCensecTipoAtoSaveSchema,
)


class TCensecTipoAtoSaveRepository(BaseRepository):
    """
    Repositório responsável pela operação de salvamento de um novo registro
    na tabela T_CENSEC_TIPOATO.
    """

    def execute(self, t_censec_tipoato_save_schema: TCensecTipoAtoSaveSchema):
        """
        Executa a operação de salvamento no banco de dados.

        Args:
            t_censec_tipoato_save_schema (TCensecTipoAtoSchema): O esquema com os dados a serem salvos.

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
                INSERT INTO T_CENSEC_TIPOATO (
                    CENSEC_TIPOATO_ID,
                    CENSEC_ID,
                    DESCRICAO,
                    SITUACAO,
                    TIPO_SEPARACAO,
                    TIPO_REVOGACAO,
                    CODIGO
                ) VALUES (
                    :censec_tipoato_id,
                    :censec_id,
                    :descricao,
                    :situacao,
                    :tipo_separacao,
                    :tipo_revogacao,
                    :codigo
                )
                RETURNING *;
            """

            # ----------------------------------------------------
            # Preenchimento dos parâmetros
            # ----------------------------------------------------
            params = {
                "censec_tipoato_id": t_censec_tipoato_save_schema.censec_tipoato_id,
                "censec_id": t_censec_tipoato_save_schema.censec_id,
                "descricao": t_censec_tipoato_save_schema.descricao,
                "situacao": t_censec_tipoato_save_schema.situacao,
                "tipo_separacao": t_censec_tipoato_save_schema.tipo_separacao,
                "tipo_revogacao": t_censec_tipoato_save_schema.tipo_revogacao,
                "codigo": t_censec_tipoato_save_schema.codigo,
            }

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
