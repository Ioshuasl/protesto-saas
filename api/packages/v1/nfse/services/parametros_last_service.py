from fastapi import HTTPException, status

from packages.v1.nfse.actions.parametros_last_action import ParametrosLastAction


class ParametrosLastService:
    def execute(self):
        action = ParametrosLastAction()
        response = action.execute()
        if not response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nao foi possivel localizar PARAMETROS para emissao de NFS-e.",
            )
        return response

