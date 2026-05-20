from packages.v1.ged.actions.ged_save_base64_payload_action import (
    GEDSaveBase64PayloadAction,
)
from packages.v1.ged.schemas.ged_schema import GEDSaveBase64RequestSchema, GEDSaveSchema
from packages.v1.ged.services.ged_save_service import GEDSaveService


class GEDSaveBase64Service:
    async def execute(self, data: GEDSaveBase64RequestSchema):
        base64_value = await GEDSaveBase64PayloadAction.execute(data)
        save_schema = GEDSaveSchema(
            serventia=int(data.path.serventia),
            pasta=str(data.path.pasta),
            registro_id=str(data.path.registro_id),
            base64=base64_value,
        )
        return GEDSaveService().execute(save_schema)
