from abstracts.repository import BaseRepository
from actions.data.prepare_update_data import prepare_update_data
from packages.v1.parametros.schemas.g_config_schema import GConfigSaveSchema


class GConfigSaveRepository(BaseRepository):

    def execute(self, data: GConfigSaveSchema):
        # ----------------------------------------------------
        # Prepara parâmetros e colunas de atualização dinâmicas
        # ----------------------------------------------------
        params, update_columns = prepare_update_data(
            data,
            exclude_fields=["config_id"],
            id_field="config_id",
        )
        # ----------------------------------------------------
        # Montagem do SQL dinâmico
        # ----------------------------------------------------
        sql = f"""
            UPDATE G_CONFIG
            SET {update_columns}
            WHERE CONFIG_ID = :config_id
            RETURNING *;
        """
        # ----------------------------------------------------
        # Execução e retorno do registro atualizado
        # ----------------------------------------------------
        return self.run_and_return(sql, params)
