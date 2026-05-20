from abstracts.repository import BaseRepository
from actions.data.prepare_update_data import prepare_update_data
from packages.v1.administrativo.schemas.t_imovel_schema import TImovelUpdateSchema
from fastapi import HTTPException, status


class TImovelUpdateRepository(BaseRepository):

    def execute(self, t_imovel_update_schema: TImovelUpdateSchema):

        try:

            params, update_columns = prepare_update_data(
                t_imovel_update_schema,
                exclude_fields=["imovel_id"],
                id_field="imovel_id",
            )

            sql = f"""
                    UPDATE T_IMOVEL
                    SET {update_columns}
                    WHERE IMOVEL_ID = :imovel_id
                    RETURNING *
                """

            # Executa o update
            response = self.run_and_return(sql, params)

            return response

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar o imóvel: {str(e)}",
            )
