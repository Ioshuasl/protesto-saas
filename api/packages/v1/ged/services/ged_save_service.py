from packages.v1.ged.actions.ged_save_action import GEDSaveAction
from packages.v1.ged.schemas.ged_schema import GEDSaveSchema


class GEDSaveService:
    def execute(self, data: GEDSaveSchema):
        save_action = GEDSaveAction()
        return save_action.execute(data)
