from abstracts.repository import BaseRepository

from actions.env.env_config_loader import EnvConfigLoader
from packages.v1.ged.schemas.ged_schema import GEDIndexSchema
from packages.v1.ged.actions.ged_delete import GedDelete


class GEDDeleteRepository(BaseRepository):
    def execute(self, data: GEDIndexSchema):
        env = EnvConfigLoader(env_file=".env")
        print(f"ORIUS_GED: {getattr(env, 'ORIUS_GED', None)}")
        base_dir = getattr(env, "GED_BASE_DIR", None) or getattr(env, "ORIUS_GED", None)

        if not base_dir:
            raise ValueError("GED_BASE_DIR/ORIUS_GED nao configurado")

        if data.serventia is None:
            raise ValueError("serventia e obrigatorio")

        deleter = GedDelete(base_dir=base_dir)

        filename = getattr(data, "filename", None)
        if not filename:
            filename = f"FOTO_A_{int(data.registro_id)}#.tif"

        result = deleter.execute(
            serventia=int(data.serventia),
            pasta=data.pasta,
            record_id=int(data.registro_id),
            filename=filename,
        )

        return {
            "original": str(result.original),
            "deleted": str(result.deleted),
            "backed_up": result.backed_up,
        }
