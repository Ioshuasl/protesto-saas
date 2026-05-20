from packages.v1.nfse.actions.parametros_save_action import ParametrosSaveAction
from packages.v1.nfse.schemas.parametros_schema import ParametrosSaveSchema


class ParametrosSaveService:
    def execute(self, data: ParametrosSaveSchema):
        action = ParametrosSaveAction()
        return action.execute(data)

