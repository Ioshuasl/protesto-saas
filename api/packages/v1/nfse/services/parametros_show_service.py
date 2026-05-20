from fastapi import HTTPException, status

from packages.v1.nfse.actions.parametros_show_action import ParametrosShowAction
from packages.v1.nfse.schemas.parametros_schema import ParametrosIdSchema


class ParametrosShowService:
    def execute(self, data: ParametrosIdSchema):
        action = ParametrosShowAction()
        response = action.execute(data)
        if not response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nao foi possivel localizar PARAMETROS.",
            )
        return response

