from fastapi import HTTPException, status
from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_censec_qualidadeato_schema import (
    TCensecQualidadeAtoSaveSchema,
)


class TCensecQualidadeAtoSaveRepository(BaseRepository):
    """
    Repositório responsável pela operação de salvamento de um novo registro
    na tabela T_CENSEC_QUALIDADEATO.
    """

    def execute(self, t_censec_qualidadeato_save_schema: TCensecQualidadeAtoSaveSchema):
        """
        Executa a operação de salvamento no banco de dados.

        Args:
            t_censec_qualidadeato_save_schema (TCensecQualidadeAtoSaveSchema):
                O esquema com os dados a serem salvos.

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
                INSERT INTO T_CENSEC_QUALIDADEATO (
                    CENSEC_QUALIDADEATO_ID,
                    CENSEC_TIPOATO_ID,
                    CENSEC_QUALIDADE_ID,
                    QTD_MINIMA
                ) VALUES (
                    :censec_qualidadeato_id,
                    :censec_tipoato_id,
                    :censec_qualidade_id,
                    :qtd_minima
                )
                RETURNING *;
            """

            # ----------------------------------------------------
            # Preenchimento dos parâmetros
            # ----------------------------------------------------
            params = {
                "censec_qualidadeato_id": t_censec_qualidadeato_save_schema.censec_qualidadeato_id,
                "censec_tipoato_id": t_censec_qualidadeato_save_schema.censec_tipoato_id,
                "censec_qualidade_id": t_censec_qualidadeato_save_schema.censec_qualidade_id,
                "qtd_minima": t_censec_qualidadeato_save_schema.qtd_minima,
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
                detail=f"Erro ao salvar registro em T_CENSEC_QUALIDADEATO: {e}",
            )
