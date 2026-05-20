from abstracts.repository import BaseRepository

from packages.v1.ged.schemas.ged_schema import GEDSaveSchema


def _get_ged_create_cls():
    from packages.v1.ged.actions.ged_create import GedCreate

    return GedCreate


class GEDSaveRepository(BaseRepository):
    """
    Repositorio responsavel pelo salvamento do arquivo GED.
    """

    def execute(self, data: GEDSaveSchema):
        quality = {
            "compression": "tiff_adobe_deflate",
            "dpi": (300, 300),
        }

        creator = _get_ged_create_cls()()

        target_path = creator.execute(
            serventia=data.serventia,
            record_id=int(data.registro_id),
            filename=None,
            base64_data=data.base64,
            pasta=data.pasta,
            quality=quality,
        )

        return {
            "absolute_path": str(target_path),
            "relative_path": str(target_path.relative_to(creator.base_dir)).replace(
                "\\", "/"
            ),
        }
