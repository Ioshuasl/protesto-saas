from actions.data.prepare_update_data import prepare_update_data
from packages.v1.administrativo.schemas.t_pessoa_schema import TPessoaSaveSchema
from fastapi import HTTPException, status
from abstracts.repository import BaseRepository


class TPessoaUpdateRepository(BaseRepository):

    def execute(self, t_pessoa_save_schema: TPessoaSaveSchema):

        try:

            params, update_columns = prepare_update_data(
                t_pessoa_save_schema, exclude_fields=["pessoa_id", "foto"], id_field="pessoa_id"
            )

            sql = f"""
                    UPDATE T_PESSOA
                    SET {update_columns}
                    WHERE PESSOA_ID = :pessoa_id
                    RETURNING pessoa_id
                """

            # Executa o update
            response = self.run_and_return(sql, params)

            return response

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar registro: {e}",
            )
