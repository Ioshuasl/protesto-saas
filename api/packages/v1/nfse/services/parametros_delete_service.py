from fastapi import HTTPException, status

from packages.v1.nfse.actions.parametros_delete_action import ParametrosDeleteAction
from packages.v1.nfse.actions.parametros_show_action import ParametrosShowAction
from packages.v1.nfse.schemas.parametros_schema import ParametrosIdSchema


class ParametrosDeleteService:
    def execute(self, data: ParametrosIdSchema):
        show_action = ParametrosShowAction()
        current = show_action.execute(data)
        if not current:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nao foi possivel localizar PARAMETROS.",
            )

        delete_action = ParametrosDeleteAction()
        deleted = delete_action.execute(data)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nao foi possivel excluir PARAMETROS.",
            )
        return deleted

