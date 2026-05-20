from abstracts.repository import BaseRepository
from actions.data.prepare_update_data import prepare_update_data
from packages.v1.administrativo.schemas.t_ato_partetipo_schema import (
    TAtoParteTipoUpdateSchema,
)
from fastapi import HTTPException, status


class TAtoParteTipoUpdateRepository(BaseRepository):

    def execute(self, t_ato_partetipo_update_schema: TAtoParteTipoUpdateSchema):

        try:

            params, update_columns = prepare_update_data(
                t_ato_partetipo_update_schema,
                exclude_fields=["ato_partipo_id"],
                id_field="ato_partipo_id",
            )

            sql = f"""
                    UPDATE T_ATO_PARTETIPO
                    SET {update_columns}
                    WHERE ATO_PARTETIPO_ID = :ato_partetipo_id
                    RETURNING ATO_PARTETIPO_ID,
                            DESCRICAO,
                            TIPO_PARTE,
                            AUTO_QUALIFICA,
                            DECLARA_DOI,
                            POSSUI_DOCUMENTO_EXT,
                            SITUACAO,
                            CENSEC_QUALIDADE_ID
                """

            # Executa o update
            response = self.run_and_return(sql, params)

            return response

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar o imóvel: {str(e)}",
            )
