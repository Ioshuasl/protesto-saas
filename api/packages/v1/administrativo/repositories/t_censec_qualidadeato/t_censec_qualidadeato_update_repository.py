from abstracts.repository import BaseRepository
from actions.data.prepare_update_data import prepare_update_data
from fastapi import HTTPException, status
from packages.v1.administrativo.schemas.t_censec_qualidadeato_schema import (
    TCensecQualidadeAtoUpdateSchema,
)


class TCensecQualidadeAtoUpdateRepository(BaseRepository):
    """
    Repositório responsável pela operação de atualização de registros
    na tabela T_CENSEC_QUALIDADEATO.
    """

    def execute(
        self, t_censec_qualidadeato_update_schema: TCensecQualidadeAtoUpdateSchema
    ):
        """
        Atualiza um registro existente na tabela T_CENSEC_QUALIDADEATO.

        Args:
            t_censec_qualidadeato_update_schema (TCensecQualidadeAtoUpdateSchema):
                Esquema contendo os dados a serem atualizados.

        Returns:
            O registro atualizado (via RETURNING *).

        Raises:
            HTTPException: Caso ocorra um erro na execução do SQL.
        """
        try:
            # ----------------------------------------------------
            # Prepara parâmetros e colunas de atualização dinâmicas
            # ----------------------------------------------------
            params, update_columns = prepare_update_data(
                t_censec_qualidadeato_update_schema,
                exclude_fields=["censec_qualidadeato_id"],
                id_field="censec_qualidadeato_id",
            )

            # ----------------------------------------------------
            # Montagem do SQL dinâmico
            # ----------------------------------------------------
            sql = f"""
                UPDATE T_CENSEC_QUALIDADEATO
                SET {update_columns}
                WHERE CENSEC_QUALIDADEATO_ID = :censec_qualidadeato_id
                RETURNING *;
            """

            # ----------------------------------------------------
            # Execução e retorno do registro atualizado
            # ----------------------------------------------------
            response = self.run_and_return(sql, params)
            return response

        except Exception as e:
            # ----------------------------------------------------
            # Tratamento de exceção e retorno HTTP padronizado
            # ----------------------------------------------------
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar registro em T_CENSEC_QUALIDADEATO: {str(e)}",
            )
