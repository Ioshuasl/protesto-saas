from abstracts.repository import BaseRepository

from actions.env.env_config_loader import EnvConfigLoader
from packages.v1.ged.actions.ged_locator import GedLocator
from packages.v1.ged.schemas.ged_schema import GEDIndexSchema


class GEDIndexRepository(BaseRepository):
    def execute(self, data: GEDIndexSchema):

        env = EnvConfigLoader(env_file=".env")
        base_dir = getattr(env, "GED_BASE_DIR", None) or getattr(env, "ORIUS_GED", None)

        if not base_dir:
            raise ValueError("GED_BASE_DIR/ORIUS_GED nao configurado")

        if data.serventia is None:
            raise ValueError("serventia e obrigatorio")

        locator = GedLocator(base_dir=base_dir)

        return locator.locate(
            serventia=int(data.serventia),
            pasta=data.pasta,
            record_id=int(data.registro_id),
            filename_contains=str(int(data.registro_id)),
            include_deleted=True,
        )
