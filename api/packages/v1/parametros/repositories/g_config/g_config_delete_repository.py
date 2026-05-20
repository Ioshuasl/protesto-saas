from abstracts.repository import BaseRepository
from packages.v1.parametros.schemas.g_config_schema import GConfigIdSchema


class GConfigDeleteRepository(BaseRepository):
    def execute(self, data: GConfigIdSchema):
        sql = """
            DELETE FROM G_CONFIG
            WHERE CONFIG_ID = :config_id
            RETURNING *
        """
        return self.run_and_return(sql, {"config_id": data.config_id})
