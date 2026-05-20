from abstracts.repository import BaseRepository
from actions.data.prepare_update_data import prepare_update_data

from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoAnteriorUpdateSchema


class TAtoAnteriorUpdateRepository(BaseRepository):
    def execute(self, t_ato_anterior_update_schema: TAtoAnteriorUpdateSchema):
        params, update_columns = prepare_update_data(
            t_ato_anterior_update_schema,
            exclude_fields=["ato_id"],
            id_field="ato_id",
        )

        sql = f"""
            UPDATE T_ATO
            SET {update_columns}
            WHERE ATO_ID = :ato_id
            RETURNING *;
        """
        return self.run_and_return(sql, params)
